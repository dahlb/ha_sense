"""Constants for ha_sense."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ha_sense"
ATTRIBUTION = "Data provided by dahlb"

CONF_SENSE_LINK = "sense_link"
CONF_DEVICES = "devices"

PLATFORMS_TO_IGNORE = ["sense", "tplink"]
