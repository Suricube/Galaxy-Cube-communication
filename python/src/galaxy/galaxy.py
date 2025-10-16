''' general galaxy class'''
from enum import Enum

# order of analog signal
class DeviceTypes(str, Enum):
    system = "system"
    device = "device"

class Galaxy:
    def __init__(self, devtype: DeviceTypes, devname: str, topic: str):
        self.device = devtype
        self.name   = devname
        self.topic  = topic
 
    def to_json(self, payload: str):
        return "{\"type\":\""+self.device+"\",\"name\":\""+self.name+"\",\"topic\":\""+self.topic+"\",\"payload\":"+payload+ "}"
