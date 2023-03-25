import logging

from homeassistant import config_entries
from homeassistant.data_entry_flow import AbortFlow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        already_exists = await self.async_set_unique_id("1")
        if already_exists is None:
            return self.async_create_entry(title="Singleton", data={})
        else:
            raise AbortFlow("already_configured")
