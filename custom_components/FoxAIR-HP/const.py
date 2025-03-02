"""Constants for the econet Integration integration."""

DOMAIN = "FoxAIR-HP"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "pblxptr, edited by ZZZ"
DEVICE_INFO_MODEL = "FoxAIR Heat Pump"
DEVICE_INFO_CONTROLLER_NAME = "FoxAIR"
DEVICE_INFO_MIXER_NAME = "Mixer"

CONF_ENTRY_TITLE = "FoxAIR-HP"
CONF_ENTRY_DESCRIPTION = "FoxAIR heat pump controller"

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
    ## Number entity
    "238": "238",
    "239": "239",
    "103": "103",
    "183": "183",
    ## Select entity
    "162": "162",
    "119": "119",
    "236": "236",
    "1231": "1231",
    ## Switch entity
}
