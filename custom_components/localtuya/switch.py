"""Platform to locally control Tuya-based switch devices."""
import logging
import tinytuya
from functools import partial

import voluptuous as vol
from homeassistant.components.switch import DOMAIN, SwitchEntity

from .common import LocalTuyaEntity, async_setup_entry
from .const import (
    ATTR_CURRENT,
    ATTR_CURRENT_CONSUMPTION,
    ATTR_VOLTAGE,
    CONF_CURRENT,
    CONF_CURRENT_CONSUMPTION,
    CONF_VOLTAGE,
)
from homeassistant.helpers import config_validation as cv, entity_platform, service

_LOGGER = logging.getLogger(__name__)


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(CONF_CURRENT): vol.In(dps),
        vol.Optional(CONF_CURRENT_CONSUMPTION): vol.In(dps),
        vol.Optional(CONF_VOLTAGE): vol.In(dps),
    }


class LocaltuyaSwitch(LocalTuyaEntity, SwitchEntity):
    """Representation of a Tuya switch."""

    def __init__(
        self,
        device,
        config_entry,
        switchid,
        **kwargs,
    ):
        """Initialize the Tuya switch."""
        super().__init__(device, config_entry, switchid, _LOGGER, **kwargs)
        self._state = None
        print("Initialized switch [{}]".format(self.name))

    @property
    def is_on(self):
        """Check if Tuya switch is on."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return device state attributes."""
        attrs = {}
        if self.has_config(CONF_CURRENT):
            attrs[ATTR_CURRENT] = self.dps(self._config[CONF_CURRENT])
        if self.has_config(CONF_CURRENT_CONSUMPTION):
            attrs[ATTR_CURRENT_CONSUMPTION] = (
                self.dps(self._config[CONF_CURRENT_CONSUMPTION]) / 10
            )
        if self.has_config(CONF_VOLTAGE):
            attrs[ATTR_VOLTAGE] = self.dps(self._config[CONF_VOLTAGE]) / 10
        return attrs

    async def async_turn_on(self, **kwargs):
        """Turn Tuya switch on."""
        await self._device.set_dp(True, self._dp_id)

    async def async_turn_off(self, **kwargs):
        """Turn Tuya switch off."""
        await self._device.set_dp(False, self._dp_id)

    async def update_energy(self):
        tinytuya.set_debug(True)      # Use tinytuya.set_debug(True,False) for windows command prompt (no color)

        d = tinytuya.OutletDevice('bf88154973e45bbb96aaci', '192.168.137.141', '932ccff3371cd2eb')
        d.set_version(3.3)

        print(" > Fetch Status < ")
        data = d.status()
        print(data)

        d.heartbeat()
        time.sleep(1)

        print(" > Request Update < ")
        result = d.updatedps([18,19,20])  # command 18
        print(result)

        print(" > Fetch Status Again < ")
        data2 = d.status()
        print(data2)

        print("")
        print("Before %r" % data)
        print("After  %r" % data2)
     
     async def async_setup_entry(hass, entry):
    """Set up the media player platform for Sonos."""

    platform = entity_platform.current_platform.get()

    # This will call Entity.set_sleep_timer(sleep_time=VALUE)
    platform.async_register_entity_service(
        SERVICE_SET_TIMER,
        {
            vol.Required('sleep_time'): cv.time_period,
        },
        "set_sleep_timer",
    ) 

    def status_updated(self):
        """Device status was updated."""
        self._state = self.dps(self._dp_id)


async_setup_entry = partial(async_setup_entry, DOMAIN, LocaltuyaSwitch, flow_schema)
