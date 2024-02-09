"""Setup ha_sense sensor platform."""
from __future__ import annotations

from sense_energy import (
    PlugInstance,
)

from logging import Logger, getLogger
from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorEntity,
    SensorDeviceClass,
)
from homeassistant.const import UnitOfPower
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity_registry import RegistryEntry
from homeassistant.helpers.event import (
    EventStateChangedData,
    async_track_state_change_event,
)
from homeassistant.helpers.typing import EventType


from .const import ATTRIBUTION, DOMAIN, CONF_DEVICES, PLATFORMS_TO_IGNORE

LOGGER: Logger = getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Find all entities in system that report Power in Watts, creating disabled Sensors matching each."""
    devices = []
    entity_registry = er.async_get(hass)
    for entity in entity_registry.entities.values():
        e: RegistryEntry = entity
        if (
            e.unit_of_measurement in [UnitOfPower.WATT, UnitOfPower.KILO_WATT]
            and e.platform not in PLATFORMS_TO_IGNORE
        ):
            if e.disabled_by is None:
                LOGGER.debug(f"{e.entity_id}:{e.device_id}")
                device_registry = dr.async_get(hass)
                hass_device: DeviceEntry = device_registry.async_get(e.device_id)
                #               LOGGER.debug(f"device:{hass_device}")
                name = e.entity_id
                common_identifier = None
                if hass_device is not None:
                    name = hass_device.name_by_user
                    for identifier in hass_device.identifiers:
                        if identifier[0] != DOMAIN:
                            common_identifier = identifier
                LOGGER.debug(f"common identifier:{common_identifier}")
                devices.append(
                    HaSenseSensorEntity(
                        name=name,
                        common_identifier=common_identifier,
                        tracked_entity_id=e.entity_id,
                    )
                )
            else:
                LOGGER.info(f"disabled energy entity: {e.entity_id}")
    async_add_devices(devices)


class HaSenseSensorEntity(SensorEntity):
    """Sensor Representing whether to Report Associated entity's power to sense device through kasa emulation."""

    _attr_attribution = ATTRIBUTION
    plug: PlugInstance = None
    unsub = None

    def __init__(
        self,
        name: str,
        common_identifier: tuple[str, str],
        tracked_entity_id: str,
    ) -> None:
        """Initialize Sensor attributes."""
        self.tracked_entity_id = tracked_entity_id
        self._attr_unique_id = f"{tracked_entity_id.partition('.')[2].replace('_electric_consumption_w', '')}_reporting_to_sense"
        if name is None:
            name = self._attr_unique_id.replace("_", " ")
        else:
            name = f"{name} reporting to sense"
        self._attr_entity_registry_enabled_default = False
        self._attr_should_poll = False
        identifiers = {(DOMAIN, self.unique_id)}
        if common_identifier is not None:
            identifiers.add(common_identifier)
        self._attr_device_info = DeviceInfo(
            identifiers=identifiers,
        )

        self.entity_description = SensorEntityDescription(
            key=self._attr_unique_id,
            name=name,
            icon="mdi:format-quote-close",
            device_class=SensorDeviceClass.POWER,
        )

    async def async_added_to_hass(self):
        """Add emulated device and a listener to update it, invoked when entity is enabled."""
        self.plug = PlugInstance(
            self._attr_unique_id, alias=self.name.replace(" reporting to sense", "")
        )
        self.hass.data[DOMAIN][CONF_DEVICES].append(self.plug)

        def state_automation_listener(_event: EventType[EventStateChangedData]):
            self._update_watts()

        self.unsub = async_track_state_change_event(
            self.hass, [self.tracked_entity_id], state_automation_listener
        )

    async def async_will_remove_from_hass(self):
        """Remove emulated device and the listener to update it, invoked when entity is disabled."""
        self.hass.data[DOMAIN][CONF_DEVICES].remove(self.plug)
        self.unsub()

    def _update_watts(self):
        entity_registry = er.async_get(self.hass)
        tracked_entity: RegistryEntry = entity_registry.async_get(
            self.tracked_entity_id
        )
        state = self.hass.states.get(self.tracked_entity_id)
        try:
            watts = float(state.state)
            if tracked_entity.unit_of_measurement == UnitOfPower.KILO_WATT:
                watts = watts * 1000
            self.plug.power = watts
        except ValueError:
            LOGGER.debug(f"{self.tracked_entity_id} watts value invalid: {state.state}")
            return
