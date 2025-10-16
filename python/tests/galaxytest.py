import sys
from galaxy import DeviceTypes, sections, Galaxy, SecOperation, SecOrder

import json

def main() -> int:

    secs = sections.Sections(SecOperation.continuous, 10000)

    # some analog sections
    sec = sections.SectionAO(0.,0.,0.,0.,100,SecOrder.linear) 
    sao = sections.SectionsAO("ao0",0)
    sao.append(sec)
    sao.append(sec)
    print(sec.to_json())
    print(sao.to_json())
    secs.appendao(sao)
 
    # some digital sections
    sec = sections.SectionDO(0,100)
    sdo = sections.SectionsDO("do0",0)
    sdo.append(sec)
    sdo.append(sec)
    print(sec.to_json())
    print(sdo.to_json())
    secs.appenddo(sdo)

    msg = Galaxy(DeviceTypes.device,"fff","ui")
    print(msg.to_json(secs.to_payload("start")))
    print(msg.to_json(secs.to_payload("set")))

    ttt= json.loads(msg.to_json(secs.to_payload("start")))
    print(ttt["topic"])
    print(type(ttt["topic"]) == str)
 
    return 0

if __name__ == '__main__':
    sys.exit(main())