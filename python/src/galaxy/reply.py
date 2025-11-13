''' galaxy reply msgs'''
from enum import Enum

class trigger(str, Enum):
    at_arrival  = "at_arrival"
    new_state   = "new_state"
    on_completion= "on_completion"

def to_replyrequest(trigger: trigger, topic: str, payload: dict, id: str)->dict:
    return {
        "trigger": trigger,
        "topic": topic,
        "payload": payload,
        "msg_id":id
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