from dataclasses import dataclass

from .common import EconetDataCoordinator, Econet300Api
from homeassistant.components.select import SelectEntityDescription, SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, SERVICE_COORDINATOR, SERVICE_API

from .common import EconetDataCoordinator, Econet300Api

from .entity import EconetEntity


@dataclass
class EconetSelectEntityDescription(SelectEntityDescription):
    """Describes Econet select entity"""


SELECT_TYPES: tuple[EconetSelectEntityDescription, ...] = (
    EconetSelectEntityDescription(
        key="1231", name="Praca pompy ciepła", options=["OFF", "ON", "Harmonogram"]
    ),
    EconetSelectEntityDescription(
        key="236", name="Tryb pracy obiegu 1", options=["OFF", "Dzień", "Noc", "Auto"]
    ),
    EconetSelectEntityDescription(
        key="119", name="Tryb pracy CWU", options=["OFF", "ON", "Harmonogram"]
    ),
    EconetSelectEntityDescription(
        key="162",
        name="Tryb Lato-Zima",
        options=["", "Lato", "Zima", "", "", "", "Auto"],
    ),
)


class EconetSelect(EconetEntity, SelectEntity):
    """Describes Econet select entity"""

    def __init__(
        self,
        description: EconetSelectEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        super().__init__(description, coordinator, api)

    def _sync_state(self, value):
        self._attr_current_option = self.options[(value["value"])]
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Update current value"""
        if not await self._api.set_param(
            self.entity_description.key, int(self.options.index(option))
        ):
            return

        self.async_write_ha_state()


def can_add(desc: EconetSelectEntityDescription, coordinator: EconetDataCoordinator):
    return coordinator.has_data(desc.key) and coordinator.data[desc.key]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSelect] = []

    for description in SELECT_TYPES:
        if can_add(description, coordinator):
            entities.append(EconetSelect(description, coordinator, api))

    return async_add_entities(entities)
