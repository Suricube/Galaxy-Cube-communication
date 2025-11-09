''' system class for galaxy controller'''
from enum import Enum

# system commands
class SystemCmds(str, Enum):
    componentlaunch = 'componentlaunch'
    componentkill   = 'componentkill'
    status          = 'status'

class System:
    def __init__(self, name: str):
        self.name = name

    def to_payload():
        return "{}"
    
    