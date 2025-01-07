"""Config flow for ElectrCosts integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN

class ElectrCostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ElectrCosts."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="ElectrCosts", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({})
        )