"""Config flow for My History."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import DOMAIN, CONF_TRACKED_ENTITIES, CONF_PURGE_DAYS

class MyHistoryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="My History", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow."""
        return MyHistoryOptionsFlowHandler()


class MyHistoryOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_entities = self.config_entry.options.get(CONF_TRACKED_ENTITIES, [])
        current_days = self.config_entry.options.get(CONF_PURGE_DAYS, 30)

        data_schema = vol.Schema({
            vol.Optional(CONF_TRACKED_ENTITIES, default=current_entities): 
                EntitySelector(EntitySelectorConfig(multiple=True)),
            vol.Optional(CONF_PURGE_DAYS, default=current_days):
                NumberSelector(NumberSelectorConfig(min=1, max=365, mode=NumberSelectorMode.BOX))
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )