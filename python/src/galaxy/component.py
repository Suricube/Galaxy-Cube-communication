''' component class for galaxy controller'''
from enum import Enum
import json

# order of analog signal
class ComponentCmds(str, Enum):
    rustplugin  = 'rustplugin'
    wasmplugin  = 'wasmplugin'
    status      = 'status'
    close       = 'close'
    abort       = 'abort'
    parsejson   = 'parsejson'

class Component:
    def __init__(self, name: str, meta: str, reply: str, version: str):
        self.name    = name
        self.meta    = meta
        self.reply   = reply
        self.version = version        

    # instantiate plugin from local rust source
    def rustplugin(self):
        pass
    # instantiate plugin from wasm
    def wasmplugin(self, wasm: str):
        pass
    # plugin status
    def get_plugin_status(self):
        pass
    # close plugin
    def plugin_close(self):
        pass

    def to_payload(self)->dict:
        return {}
    
    def to_msg(self)->str:
        msg = {
            "command": "component", 
            "tasks": [ 
                    {
                        "component_cmd": "execute_json_command",
                        "component_name": self.name,
                        "payload":{
                            "meta":"dd",
                            "ss":self.to_payload(),
                            "reply":"sss"
                            }
                    }
                ]
            }
        return json.dumps(msg)
