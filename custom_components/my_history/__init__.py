"""My History integration."""
import logging
import os
import yaml
import aiofiles
from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import frontend
from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN, CONF_TRACKED_ENTITIES, CONF_PURGE_DAYS
from .panel import MyHistoryPanelView

_LOGGER = logging.getLogger(__name__)

# Track panel registration in hass.data instead of global variable
PANEL_REGISTERED_KEY = "panel_registered"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    _LOGGER.info(f"========== SETUP ENTRY CALLED ==========")
    _LOGGER.info(f"Entry ID: {entry.entry_id}")
    
    # FORCE REMOVE any existing panel at startup - this ensures a clean slate
    try:
        frontend.async_remove_panel(hass, "my-history")
        _LOGGER.info("Force-removed any existing panel at startup")
    except (ValueError, KeyError):
        _LOGGER.debug("No existing panel to remove at startup")
        pass
    
    # Get configuration from options
    tracked = entry.options.get(CONF_TRACKED_ENTITIES, [])
    purge_days = entry.options.get(CONF_PURGE_DAYS, 30)
    
    _LOGGER.info(f"Tracking {len(tracked)} excluded entities, purge days: {purge_days}")
    
    # Initialize domain data if needed
    hass.data.setdefault(DOMAIN, {})
    
    # Check if this entry is already set up
    if entry.entry_id in hass.data[DOMAIN]:
        _LOGGER.warning(f"Entry {entry.entry_id} already set up! Updating data...")
    
    # Store configuration
    hass.data[DOMAIN][entry.entry_id] = {
        "tracked_entities": tracked,
        "purge_keep_days": purge_days,
    }
    
    # Track panel registration status in hass.data
    hass.data[DOMAIN].setdefault(PANEL_REGISTERED_KEY, False)
    
    # Register HTTP views (these are safe to register multiple times)
    hass.http.register_view(MyHistoryPanelView)
    hass.http.register_view(MyHistorySaveView)
    
    # Register sidebar panel (with duplicate prevention)
    await async_register_panel(hass, entry)
    
    # Register service for WebSocket calls (optional, keep for compatibility)
    await async_register_services(hass, entry)
    
    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    # Generate initial recorder config
    await generate_recorder_config(hass, tracked, purge_days)
    
    _LOGGER.info(f"========== SETUP ENTRY COMPLETE ==========")
    return True

async def async_register_services(hass: HomeAssistant, entry: ConfigEntry):
    """Register services for WebSocket calls."""
    
    async def handle_update_selections(call):
        """Handle the update_selections service call."""
        _LOGGER.debug("Service update_selections called")
        
        tracked = call.data.get("tracked_entities", [])
        purge_days = call.data.get("purge_keep_days", 30)
        
        _LOGGER.info(f"Service updating {len(tracked)} excluded entities, purge days: {purge_days}")
        
        # Update options
        new_options = {
            CONF_TRACKED_ENTITIES: tracked,
            CONF_PURGE_DAYS: purge_days
        }
        
        hass.config_entries.async_update_entry(entry, options=new_options)
        
        return {"success": True, "count": len(tracked)}
    
    # Register the service
    hass.services.async_register(DOMAIN, "update_selections", handle_update_selections)
    _LOGGER.debug("Services registered successfully")

async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry):
    """Register the sidebar panel with strong duplicate prevention."""
    
    # Check if panel is already registered in this session
    if hass.data[DOMAIN].get(PANEL_REGISTERED_KEY, False):
        _LOGGER.debug("Panel already registered in this session, skipping")
        return
    
    # Always try to remove any existing panel first (cleanup)
    try:
        frontend.async_remove_panel(hass, "my-history")
        _LOGGER.debug("Removed any existing panel before registration")
    except (ValueError, KeyError):
        _LOGGER.debug("No existing panel to remove before registration")
        pass
    
    # Register new panel - using iframe with sandbox disabled
    frontend.async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="My History",
        sidebar_icon="mdi:history",
        frontend_url_path="my-history",
        config={
            "url": f"/api/my_history/panel/{entry.entry_id}",
        },
        require_admin=True,
    )
    
    # Mark as registered
    hass.data[DOMAIN][PANEL_REGISTERED_KEY] = True
    _LOGGER.info("Panel registered successfully")

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update when options change."""
    _LOGGER.debug("Options updated, reloading data")
    
    # Get updated configuration
    tracked = entry.options.get(CONF_TRACKED_ENTITIES, [])
    purge_days = entry.options.get(CONF_PURGE_DAYS, 30)
    
    # Update hass.data
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.entry_id].update({
            "tracked_entities": tracked,
            "purge_keep_days": purge_days,
        })
        _LOGGER.info(f"Updated tracking: {len(tracked)} entities, {purge_days} days")
    else:
        _LOGGER.error(f"Entry {entry.entry_id} not found in hass.data")
    
    # Generate complete recorder config
    await generate_recorder_config(hass, tracked, purge_days)

async def generate_recorder_config(hass: HomeAssistant, tracked_entities: list, purge_days: int):
    """Generate the complete recorder_config.yaml file."""
    config_dir = hass.config.path()
    yaml_path = os.path.join(config_dir, "recorder_config.yaml")
    
    # Structure the complete recorder config
    yaml_data = {
        "purge_keep_days": purge_days,
        "exclude": {
            "entities": tracked_entities
        }
    }
    
    try:
        # Convert dict to YAML string
        yaml_str = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
        
        # Write file asynchronously using aiofiles
        async with aiofiles.open(yaml_path, 'w') as f:
            await f.write(yaml_str)
            
        _LOGGER.info(f"Generated {yaml_path} with purge_keep_days: {purge_days}, {len(tracked_entities)} excluded entities")
    except Exception as e:
        _LOGGER.error(f"Failed to write recorder config: {e}")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload config entry."""
    _LOGGER.info(f"Unloading My History integration")
    
    # Remove services
    hass.services.async_remove(DOMAIN, "update_selections")
    
    # Remove panel
    try:
        frontend.async_remove_panel(hass, "my-history")
        _LOGGER.debug("Panel removed")
    except (ValueError, KeyError):
        _LOGGER.debug("Panel already removed")
        pass
    
    # Reset panel registration flag
    if DOMAIN in hass.data:
        hass.data[DOMAIN][PANEL_REGISTERED_KEY] = False
    
    # Remove entry data
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug(f"Removed entry {entry.entry_id} from hass.data")
    
    # Optionally remove the recorder config file? 
    # Commenting out - usually better to leave it
    # try:
    #     config_dir = hass.config.path()
    #     yaml_path = os.path.join(config_dir, "recorder_config.yaml")
    #     if os.path.exists(yaml_path):
    #         os.remove(yaml_path)
    #         _LOGGER.debug(f"Removed {yaml_path}")
    # except Exception as e:
    #     _LOGGER.error(f"Failed to remove recorder config: {e}")
    
    return True


class MyHistorySaveView(HomeAssistantView):
    """HTTP View to save selections from the panel - NO AUTH REQUIRED."""
    
    url = "/api/my_history/selections"
    name = "api:my_history:selections"
    requires_auth = False  # CRITICAL: This allows iframe to save without tokens

    async def post(self, request):
        """Handle POST request with selections."""
        hass = request.app["hass"]
        
        try:
            data = await request.json()
            _LOGGER.debug(f"Save request received with {len(data.get('tracked_entities', []))} entities")
            
            # Validate data
            if not isinstance(data, dict):
                return web.Response(status=400, text="Invalid JSON data")
            
            # Find the config entry (there should only be one)
            entries = hass.config_entries.async_entries(DOMAIN)
            if not entries:
                _LOGGER.error("No config entries found")
                return web.Response(status=404, text="Integration not found")
            
            entry = entries[0]
            
            # Update options
            new_options = {
                CONF_TRACKED_ENTITIES: data.get("tracked_entities", []),
                CONF_PURGE_DAYS: data.get("purge_keep_days", 30)
            }
            
            hass.config_entries.async_update_entry(entry, options=new_options)
            _LOGGER.info(f"Saved {len(new_options[CONF_TRACKED_ENTITIES])} excluded entities")
            
            return web.Response(status=200, text="OK")
            
        except Exception as e:
            _LOGGER.error(f"Error saving selections: {e}", exc_info=True)
            return web.Response(status=500, text=str(e))