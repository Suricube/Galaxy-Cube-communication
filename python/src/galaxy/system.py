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
    componentabort  = 'componentabort'
    componentclose  = 'componentclose'
    componentstatus = 'componentstatus'
    status          = 'status'
    activecomponents= 'GetActiveComponents'
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
            case SystemCmds.activecomponents:
                pass
            case _:
                pass
        return msg

    # status
    def get_status(self, socket: GalaxySocket)->Future:
        self.cmd = SystemCmds.componentlaunch
        return socket.sendawait(self.to_msg(), self.get_status_reply)

    def get_status_reply(self, payload: dict)->Result[str, str]:
        status = payload.get("status", None)
        if status is None:
            return Err('System: parsing error in capabilities')
        self.status = status
        return Ok("received status data")

    # launch new component
    def launch_component(self, socket: GalaxySocket)->Future:
        self.cmd = SystemCmds.componentlaunch
        return socket.sendawait(self.to_msg(), self.launch_component_reply)

    def launch_component_reply(self, payload: dict)->Result[str, str]:
        status = payload.get("status", None)
        if status is None:
            return Err('System: parsing error in capabilities')
        self.status = status
        return Ok("received status data")

    # close component
    def close_component(self, socket: GalaxySocket)->Future:
        self.cmd = SystemCmds.componentclose
        return socket.sendawait(self.to_msg(), self.close_component_reply)

    def close_component_reply(self, payload: dict)->Result[str, str]:
        status = payload.get("status", None)
        if status is None:
            return Err('System: parsing error in capabilities')
        self.status = status
        return Ok("received status data")

    # Capabilities
    def get_activecomponents(self, socket: GalaxySocket)->Future:
        self.cmd = SystemCmds.activecomponents
        return socket.sendawait(self.to_msg(), self.set_capabilities)
 
    def set_capabilities(self, payload: dict)->Result[str, str]:
        caps = payload.get("caps", None) 
        if caps is None:
            return Err('System: parsing error in capabilities')
        self.caps = caps
        return Ok("received caps data")
    