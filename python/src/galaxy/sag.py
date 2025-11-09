import sys
import json
from .component import Component

''' galaxy section claas'''
from enum import Enum

# section types
class SecCommands(str, Enum):
    set_sections  = "set_sections"
    clear_sections= "clear_sections"
    set_settings  = "set_settings"
    
# order of analog signal
class SecOrder(str, Enum):
    constant = 'constant'
    linear   = 'linear'
    square   = 'square'
    cubic    = 'cubic'

# overwrite options for analog signal
class SecTransition(str, Enum):
    continuous     = 'continuous'
    discontinuous  = 'discontinuous'

    # section types
class SecRepetions(str, Enum):
    finite     = 'finite'
    continuous = 'continuous'

class SecTimeUnits(str,Enum):
    ticks = 'ticks'
    us    = 'us'
    ms    = 'ms'
    s     = 's'

class SectionAO:
    def __init__(self,yl: float,yr:float,dl:float,dr:float,t: float, tunits: SecTimeUnits,s: SecOrder):
        self.yl:float = yl
        self.yr:float = yr
        self.dl:float = dl
        self.dr:float = dr
        self.n: float = t
        self.tuints: SecTimeUnits = tunits
        self.order:SecOrder = s
        #  "shifts": [1, 20, 20],

    def to_dict(self):
        msg =   {
                    "duration" : {
                        self.tuints: self.n
                    }, 
                    "starting_level" : self.yl, 
                    "ending_level": self.yr, 
                    "starting_derivative": self.dl, 
                    "ending_derivative": self.dr,
                    "interpolation": self.order,
                }
        return msg

    def to_poly(self):
        """ ensure a minimal section length of 1"""
        if self.n<1:
            self.n=1

        """ continuous and discontinous cases"""
        self.p0 = self.yl
        match self.order:
            case SecOrder.constant:
                self.p1 = 0.
                self.p2 = 0.
                self.p3 = 0.
            case SecOrder.linear:
                self.p1 = (self.yr-self.yl)/self.n
                self.p2 = 0.
                self.p3 = 0.
            case SecOrder.square:
                if self.n>=2:
                    self.p1 = self.dl/self.n
                    self.p2 = 2.*(self.yr-self.yl-self.dl)/self.n/(self.n-1.)
                    self.p3 = 0.
                else:
                    self.p1 = (self.yr-self.yl)/self.n
                    self.p2 = 0.
                    self.p3 = 0.

            case SecOrder.cubic:
                if self.n>=3:
                    self.p1 = self.dl/self.n
                    self.p2 = (6.*(self.yr-self.yl-self.dl)-2.*(self.dr-self.dl))/self.n/(self.n-1.)
                    self.p3 = 6.*(self.dl+self.dr - 2.*(self.yr-self.yl))/self.n/(self.n-1.)/(self.n-2.)
                elif self.n==2:
                    self.p1 = self.dl/self.n
                    self.p2 = 2.*(self.yr-self.yl-self.dl)/self.n/(self.n-1.)
                    self.p3 = 0.
                else:
                    self.p1 = (self.yr-self.yl)/self.n
                    self.p2 = 0.
                    self.p3 = 0.

        print(self.p0,self.p1,self.p2,self.p3)

    def iter(self):
        self.p0 = self.p0 + self.p1
        self.p1 = self.p1 + self.p2
        self.p2 = self.p2 + self.p3

    def to_json(self):
        return json.dumps(self.to_dict)

class Transition:
    def __init__(self, index: int, type: SecTransition):
        self.index = index
        self.type  = type
    def to_dict(self):
        return {"number":self.index,"transition":self.type}

    

# analog section
class SAG(Component):
    def __init__(self,name: str = "ASG0", meta: str = "", reply: str="", version: str = "0.0.1"):
        Component.__init__(self,name, meta, reply, version)
        self.up_shift: int    = 20
        self.down_shift: int  = 20
        self.clocks_per_cycle: int = 4
        self.repetitions = SecRepetions.finite
        self.sections:    list[SectionAO] = []
        self.transitions: list[Transition] = []
        self.version: str = version
        self.cmd = SecCommands.set_sections

    def set_properties(self,repetitions: SecRepetions = SecRepetions.continuous):
            self.repetitions = repetitions
            
    # sections
    def append_section(self, sec: SectionAO):
        self.sections.append(sec)

    def new_section(self, sec: list[SectionAO]):
        self.sections.append(sec)

    def clear_sections(self):
       self.sections: list[SectionAO] = []

    # transitions
    def new_transitions(self, transitions: list[Transition]):
        self.transitions.append(transitions)

    def append_transitions(self, transitions: Transition):
        self.transitions.append(transitions)

    def clear_transitions(self):
            self.transitions: list[Transition] = []

    def sections_to_msg(self) -> dict:
        sections = [ob.to_dict() for ob in self.sections]
        if self.transitions == []:
            transitions = [Transition(index,SecTransition.discontinuous).__dict__ for index in range(len(self.sections))]
        else:
            transitions = [ob.to_dict() for ob in self.transitions]
        msg = {
                "set_voltage_signal": {
                    "sections": sections,
                    "repetitions": self.repetitions,
                },
            "section_order": transitions,
            },
        return msg

    def to_payload(self):
        match self.cmd:
            case SecCommands.set_settings:
                return self.settings_to_msg()
            case SecCommands.set_sections:
                return self.sections_to_msg()
            case _:
                return "{}"
    
    def settings_to_msg(self) -> dict:
        msg = {
            "set_settings": {
                "up_shifting": self.up_shift,
                "down_shifting": self.down_shift,
                "clocks_per_cycle": self.clocks_per_cycle,
                "fpga_clock_freq": 124998749.0,
                "a": 0.00015,
                "b": -5.0,
                "repetitions": "infinite",
                "trigger_module_selection": 255,
                "driver_selection": 3,
                "SLICE_STARTING_BYTE": 0,
                "ORDER_STARTING_BYTE": 400,
            },
            "reply":[
                {
                    "timing": "at_arrival", # after_processing , after x s
                    "topic": "xxx", 
                    "payload": {}
                }
            ]
        }
        return msg

