# mock system reply messages
from result import Ok, Err, Result, is_ok, is_err

class capability:
    def __init__(self, name,status):
        self.name = name
        self.id = uuid.uuid3(uuid.NAMESPACE_DNS,name)
        self.status= status

    def to_dict(self):
        return {"name":self.name,"id":str(self.id),"status":self.status}

capabilities : list[capability] = [capability("ASG_0","running"),capability("ASG_1","running")]

def system_paring(payload: dict)->Result[dict, str]:
    cmd = payload.get("cmd",None)
    id = payload.get("reply",{}).get("msg_id", None)
    if cmd is None:
        return Err("No cmd in payload")
    rpayload = {}
    match dict["cmd"]:
        case "status":
            pass
        case "capabilities":
            caps = [ob.to_dict() for ob in capabilities]
            rpayload = {
                "cmd":"set_capabilities",
                "msg_id": id,
                "caps":caps,
            }
        case _:
            rpayload = {"error":"wrong command"}

    return Ok(rpayload)
