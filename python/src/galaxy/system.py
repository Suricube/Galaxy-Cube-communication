''' system class for galaxy controller'''
from enum import Enum
import json
from .component import Component
import asyncio
from .socket import GalaxySocket
from asyncio import Future
from result import Ok, Err, Result, is_ok, is_err

VERSION = "0.1.0"

# system commands
class SystemCmds(str, Enum):
    componentlaunch = 'componentlaunch'
    componentkill   = 'componentkill'
    status          = 'status'
    capabilities    = 'capabilities'
    storewasm       = 'storewasm'
    storeconfig     = 'storeconfig'
    getconfig       = 'getconfig'

class System(Component):
    def __init__(self):
        Component.__init__(self, "system", VERSION)
        self.caps = {}

    def to_payload(self)->dict:
        msg = {}
        match self.cmd:
            case "capabilities":
                pass
            case _:
                pass
        return msg

    def get_capabilities(self, socket: GalaxySocket)->Future:
        return socket.sendawait(self.to_msg(), self.set_capabilities)
 
    def set_capabilities(self, payload: dict)->Result[str, str]:
            print("in set caps")
            print(payload)
            caps = payload.get("caps", None) 
            if caps is None:
                return Err('User does not exist')
            self.caps = caps
            return Ok("caps worked")
    