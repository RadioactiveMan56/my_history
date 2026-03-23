"""View for My History panel."""
import logging
from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers import device_registry as dr, entity_registry as er

from ..const import DOMAIN
from .html_generator import generate_panel_html

_LOGGER = logging.getLogger(__name__)

class MyHistoryPanelView(HomeAssistantView):
    """View to serve the HTML panel with device filtering."""

    url = "/api/my_history/panel/{entry_id}"
    name = "api:my_history:panel"
    requires_auth = False

    async def get(self, request, entry_id):
        """Handle GET request - generate HTML panel."""
        hass = request.app["hass"]
        
        # Get tracked entities from hass.data
        data = hass.data.get(DOMAIN, {}).get(entry_id, {})
        tracked = data.get("tracked_entities", [])
        purge_days = data.get("purge_keep_days", 30)
        
        # Get all entities with their states
        all_states = hass.states.async_all()
        
        # Get device registry for device information
        device_reg = dr.async_get(hass)
        devices = list(device_reg.devices.values())
        
        # Get entity registry
        entity_reg = er.async_get(hass)
        
        # Create a lookup for device names
        device_names = {device.id: device.name_by_user or device.name or "Unnamed Device" for device in devices}
        
        # Build entity list with device info
        entities = []
        for state in all_states:
            entity_id = state.entity_id
            
            # Get registry entry if it exists
            registry_entry = entity_reg.async_get(entity_id)
            
            device_id = registry_entry.device_id if registry_entry else None
            device_name = device_names.get(device_id, "No Device") if device_id else "No Device"
            
            entity_data = {
                "entity_id": entity_id,
                "name": state.attributes.get("friendly_name", entity_id),
                "device_id": device_id or "",
                "device_name": device_name,
                "domain": entity_id.split('.')[0],
                "selected": entity_id in tracked,
                "state": state.state,
            }
            entities.append(entity_data)
        
        # Sort entities by device then name
        entities.sort(key=lambda x: (x["device_name"], x["name"]))
        
        # Generate HTML using the modular generator
        html = generate_panel_html(entities, devices, device_names, tracked, purge_days)
        
        return web.Response(text=html, content_type="text/html")