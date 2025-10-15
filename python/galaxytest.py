import sys
import galaxy
import sections
from sections import SecOrder, SecOperation
from galaxy import DeviceTypes

def main() -> int:

    secs = sections.Sections("foo",SecOperation.continuous, 10000)

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

    msg = galaxy.Galaxy(DeviceTypes.device,"fff")
    print(msg.to_json(secs.to_payload("start")))
    print(msg.to_json(secs.to_payload("set")))

    return 0

if __name__ == '__main__':
    sys.exit(main())