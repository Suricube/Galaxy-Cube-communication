import json
import sys
from enum import Enum

class SecTimeUnits(str,Enum):
    ticks = 'ticks'
    us    = 'us'
    ms    = 'ms'
    s     = 's'
    
class SectionDO:
    def __init__(self, t: float, units: SecTimeUnits, value: bool):
        self.duration = t
        self.units = units
        self.value = value
    def to_dict(self):
        return {"value":self.value,"duration":{self.units:self.duration}}


class SDG:
    def __init__(self, name: str = "SGO_0"):
        self.name = name
        self.sections: list[SectionDO] = []
    
    def append_section(self, s: SectionDO):
        self.sections.append(s)

    def clear_sections(self, s: SectionDO):
        self.sections: list[SectionDO] = []

    def new_sections(self, s: list[SectionDO]):
        self.sections = s

    def to_json(self):
        sections = [ob.to_dict() for ob in self.sections]
        msg = {
                "command":"function_component",
                "parameters": {
                "actor_name": self.name,
                "function_name": "execute_json_command",
                "set_digital_signal": {
                    "sections" : sections, 
                }
                }
            }
        return json.dumps(msg)


def main() -> int:

    sdg = SDG("SDO_0")
    sec = SectionDO(10,SecTimeUnits.ms,True)
    sdg.append_section(sec)
    sec = SectionDO(10,SecTimeUnits.ms,False)
    sdg.append_section(sec)
    print(sdg.to_json())

    return 0



if __name__ == '__main__':
    sys.exit(main())