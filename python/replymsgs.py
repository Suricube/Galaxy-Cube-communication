''' galaxy section claas'''
from enum import Enum

msg = {
    "reply": [{
                    "timing": "at_arrival", # after_processing , after x s
                    "topic": "xxx", 
                    "payload": {}
                }]
}

class timing(str, Enum):
    at_arrival  = "at_arrival"
    new_state   = "new_state"


msg = {
    "meta":{
        "msg_id":"uuic", # unique message id, used to asign replies to messages in async framework
        "desc":"some infos about the message",
        "version":"0.1.0",
        "comp_id":"uuic" # unique component id
    }
}

class GalaxyErrors(str, Enum):
    none                = "none"
    json_parsing        = "json_parsing"
    json_missing_field  = "json_missing_field"
    comp_not_found      = "component_not_found"
    Comp_wrong_cmd      = "component_wrong_cmd"
    comp_json_parsing   = "component_json_parsing"
    comp_wrong_version  = "component_wrong_version"
    sys_json_parsing    = "system_json_parsing"
    sys_json_wrong_cmd  = "system_json_wrong_cmd"
    sys_wrong_version   = "system_wrong_version"