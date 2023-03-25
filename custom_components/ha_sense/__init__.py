"""Create ha sense integration."""
from __future__ import annotations

from sense_energy import (
    SenseLink,
)
from asyncio import sleep
from logging import Logger, getLogger
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

from .const import (
    DOMAIN,
    CONF_DEVICES,
    CONF_SENSE_LINK,
)

LOGGER: Logger = getLogger(__package__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Create instance of integration."""
    LOGGER.debug("async_setup_entry")
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    data = {CONF_DEVICES: []}

    def devices():
        return data[CONF_DEVICES]

    data[CONF_SENSE_LINK] = SenseLink(devices)

    hass.data.setdefault(DOMAIN, data)
    await data[CONF_SENSE_LINK].start()

    def debug(_event):
        LOGGER.debug("printing instance wattages")
        for inst in data[CONF_DEVICES]:
            LOGGER.debug(f"Plug {inst.alias} power: {inst.power}")
        data[CONF_SENSE_LINK].print_instance_wattages()

    async_track_time_interval(hass, debug, timedelta(minutes=2))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Free all resources used by integration."""
    LOGGER.debug("async_unload_entry")
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN]
        LOGGER.debug("stopping listener")
        await data[CONF_SENSE_LINK].stop()
        await sleep(
            5
        )  # pause to allow port to be freed in case trying to reuse it, aka reloading integration
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Free and reinit."""
    LOGGER.debug("async_reload_entry")
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
