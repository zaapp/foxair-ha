"""Constants for the econet Integration integration."""

DOMAIN = "econet300"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

## Sys params
API_SYS_PARAMS_URI = "sysParams"
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"

## Reg params
API_REG_PARAMS_URI = "regParams"
API_REG_PARAMS_PARAM_DATA = "curr"

## Modify params
API_CONFIG_PARAMS_URI = "editParams"
API_CONFIG_PARAMS_DATA = "data"

EDITABLE_PARAMS_MAPPING_TABLE = {
    "238": "238",
    "239": "239",
    "103": "103",
    "183": "183",
}
