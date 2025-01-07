"""Platform for sensor integration."""
from __future__ import annotations
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from datetime import timedelta
import logging
import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the ElectrCosts sensor platform from a config entry."""
    _LOGGER.debug("Setting up ElectrCosts sensor platform from config entry: %s", config_entry)
    async_add_entities([ElectrCostsSensor()])
    _LOGGER.debug("ElectrCosts sensor platform setup complete")

class ElectrCostsSensor(SensorEntity):
    """Representation of an ElectrCosts sensor."""

    @property
    def icon(self) -> str:
        return 'mdi:cash'

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        return "Kč"        


    def __init__(self):
        """Initialize the sensor."""
        _LOGGER.debug("Initializing ElectrCosts sensor")
        
        self._attr_name = "ElectrCosts Sensor"
        self._attr_native_value = 0.0
        self._attr_unique_id = "electrcosts_sensor_1"  # Přidání jedinečného ID
        #self._attr_unit_of_measurement = "CZK"
        self._attr_unit_of_measurement = "Kč"        
        self._attr_device_class = None
        self._attr_device_state_class = SensorStateClass.TOTAL
        self._update_interval = timedelta(seconds=20)
        self._resource = "http://185.15.110.81/cgi_s0d"
        
        _LOGGER.debug("ElectrCosts sensor initialized with update interval: %s", self._update_interval)
        _LOGGER.debug("ElectrCosts sensor State: %s, Type: %s, Unit: %s", self._attr_state, type(self._attr_state), self._attr_unit_of_measurement)



    async def async_added_to_hass(self):
        """Register update interval."""
        _LOGGER.debug("Adding ElectrCosts sensor to Home Assistant")
        self._unsub_update = async_track_time_interval(
            self.hass, self._update, self._update_interval
        )
        self.async_write_ha_state()
        
        _LOGGER.debug("ElectrCosts sensor added to Home Assistant with update interval")

    async def async_will_remove_from_hass(self):
        """Unregister update interval."""
        _LOGGER.debug("Removing ElectrCosts sensor from Home Assistant")
        self._unsub_update()
        _LOGGER.debug("ElectrCosts sensor removed from Home Assistant")

    async def _update(self, _):
        """Update the sensor state."""
        _LOGGER.debug("Updating ElectrCosts sensor state")
        async with aiohttp.ClientSession() as session:
            async with session.get(self._resource) as response:
                if response.status == 200:
                    value = await response.text()
                    _LOGGER.debug("Received data: %s", value)
                    val1 = self._extract_value(value, 15)
                    val2 = self._extract_value(value, 16)
                    self._attr_native_value = round((val1 + val2),2)
#                    _LOGGER.debug("Updated sensor state to: %s", self._attr_state)
                    _LOGGER.debug("Updated state: %s (type=%s)", self._attr_state, type(self._attr_state))
                else:
                    _LOGGER.error("Error fetching data from %s: %s", self._resource, response.status)
        self.async_write_ha_state()
        _LOGGER.debug("async_write_ha_state called successfully")

    def _extract_value(self, value, index):
        """Extract value from the response."""
        import re
        match = re.findall(r'(?:\|[^|]*){' + str(index) + r'}\|([^|]*)', value)
        if match:
            return float(match[0].replace(' CZK', ''))
        return 0.0