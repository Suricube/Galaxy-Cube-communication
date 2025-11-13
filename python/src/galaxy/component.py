''' component class for galaxy controller'''
from enum import Enum
import json
from .meta import to_meta
from .reply import to_replyrequest, trigger
import uuid

# order of analog signal
class ComponentCmds(str, Enum):
    rustplugin  = 'rustplugin'
    wasmplugin  = 'wasmplugin'
    status      = 'status'
    close       = 'close'
    abort       = 'abort'
    parsejson   = 'parsejson'

class Component:
    def __init__(self, name: str, version: str):
        self.name    = name
        self.meta    = {}
        self.replyrequest = {}
        self.version = version
        self.cmd = None

    def set_meta(self, desc: str):
        self.meta = to_meta(desc, self.version)
        return self
    
    def set_reply(self, trigger: trigger, topic: str, payload: dict):
        id = str(uuid.uuid1())
        self.replyrequest = to_replyrequest(trigger, topic, payload, id)
        return self

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

    # overwritten by specific component implementation
    #@overwrite abc.abstractmethod
    def to_payload(self)->dict:
        return {}
    
    def to_msg(self)->str:
        msg = {
#            "command": "component", 
#            "tasks": [ 
#                    {
                        "command": "execute_json_command",
                        "name": self.name,
                        "payload":{
                            "cmd":self.cmd,
                            "meta":self.meta,
                            "parameters":self.to_payload(),
                            "reply":self.replyrequest
                            }
                    }
#                ]
#            }
        return json.dumps(msg)
