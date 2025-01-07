"""ElectrCosts integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the ElectrCosts integration."""
    _LOGGER.info("Setting up ElectrCosts integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ElectrCosts from a config entry."""
    _LOGGER.info("Setting up ElectrCosts from config entry")
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload ElectrCosts config entry."""
    _LOGGER.info("Unloading ElectrCosts config entry")
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True