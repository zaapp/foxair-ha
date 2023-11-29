from abc import ABC
from dataclasses import dataclass
from typing import Callable, Any

from .common import EconetDataCoordinator, Econet300Api
from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass, SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, SERVICE_COORDINATOR, SERVICE_API

import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes Econet sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


SENSOR_TYPES: tuple[EconetSensorEntityDescription, ...] = (
    EconetSensorEntityDescription(
        key="TempBuforUp",
        name="Temperatura bufora GÓRA",
        icon="mdi:thermometer",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="TempBuforDown",
        name="Temperatura burora DÓŁ",
        icon="mdi:thermometer",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="TempWthr",
        name="Temperatura zewnętrzna",
        icon="mdi:thermometer",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="PHNXreg2045",
        name="Temperatura zasilania pompy ciepła",
        icon="mdi:thermometer",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x/10, 2)
    ),
    EconetSensorEntityDescription(
        key="PHNXreg2046",
        name="Temperatura powrotu pompy ciepła",
        icon="mdi:thermometer",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x/10, 2)
    ),
    EconetSensorEntityDescription(
        key="Circuit1thermostat",
        name="Temperatura termostat 1",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="TempCWU",
        name="Temperatura CWU",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="ElectricPower",
        name="Zużycie energii",
        native_unit_of_measurement="kW",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="HPStatusWorkMode",
        name="Zawór trójdrogowy",
        device_class=SensorDeviceClass.ENUM,
        options=[0,1,2],
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="PHNXreg2071",
        name="Częstotliwość sprężarki",
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.FREQUENCY,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="PHNXreg2074",
        name="Obroty wentylatora",
        native_unit_of_measurement="obr/min",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.FREQUENCY,
        process_val=lambda x: round(x, 2)
    ),
    EconetSensorEntityDescription(
        key="BuforCalcSetTemp",
        name="Temperatura zadana bufora",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2)
    ),
)


class EconetSensor(SensorEntity):
    """"""

    def _sync_state(self, value):
        """Sync state"""
        _LOGGER.debug("Update EconetSensor entity:" + self.entity_description.name)

        self._attr_native_value = self.entity_description.process_val(value)

        self.async_write_ha_state()


class ControllerSensor(EconetEntity, EconetSensor):
    """"""

    def __init__(self, description: EconetSensorEntityDescription, coordinator: EconetDataCoordinator,
                 api: Econet300Api):
        super().__init__(description, coordinator, api)


def can_add(desc: EconetSensorEntityDescription, coordinator: EconetDataCoordinator):
    return coordinator.has_data(desc.key) and coordinator.data[desc.key] is not None


def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    entities = []

    for description in SENSOR_TYPES:
        if can_add(description, coordinator):
            entities.append(ControllerSensor(description, coordinator, api))
        else:
            _LOGGER.debug("Availability key: " + description.key + " does not exist, entity will not be "
                                                                   "added")

    return entities


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSensor] = []
    entities = entities + create_controller_sensors(coordinator, api)

    return async_add_entities(entities)
