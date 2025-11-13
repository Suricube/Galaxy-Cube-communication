''' a mock emulating the Galaxy controller '''
import asyncio
import aiomqtt
import json
import uuid

def warp_payload(name: str, payload: dict):
    msg = {
        "command":"execute_json_command",
        "name":name,
        "payload":payload
    }
    return msg

class capability:
    def __init__(self, name,status):
        self.name = name
        self.id = uuid.uuid3(uuid.NAMESPACE_DNS,name)
        self.status= status

    def to_dict(self):
        return {"name":self.name,"id":str(self.id),"status":self.status}

capabilities : list[capability] = [capability("ASG_0","running"),capability("ASG_1","running")]

async def listen():
    async with aiomqtt.Client("localhost", identifier="mock",clean_session=True) as client:
        await client.subscribe("ui")
        async for message in client.messages:
            print("msg")
            print("msg: "+message.payload.decode("utf-8"))
            value = json.loads(message.payload.decode("utf-8"))
            name = value["name"]
            payload = value.get("payload")
            msg = {}
            match name.lower():
                case "system":
                    cmd = payload["cmd"]
                    id = payload.get("reply",{}).get("msg_id", None)
                    print(name+" -> "+cmd+"  id: "+id)
                    match cmd:
                        case "capabilities":
                            caps = [ob.to_dict() for ob in capabilities]
                            rpayload = {
                                "cmd":"set_capabilities",
                                "msg_id": id,
                                "caps":caps,
                            }
                        case _:
                            rpayload = {"error":"wrong command"}

                case "asg_0":
                    cmd = payload["cmd"]
                    id = payload.get("reply",{}).get("msg_id", None)
                    print(name+" -> "+cmd+"  id: "+id)
                    rpayload = {
                        "cmd":cmd,
                        "msg_id": id,
                    }
                case _:
                    print(name)
                    rpayload = {"error":"component not found"}
            print(json.dumps(rpayload))
            await client.publish("galaxy",payload=json.dumps(warp_payload(name, rpayload)))

        async def disconnect(self):
            await self.c.disconnect()

async def main():
    loop = asyncio.get_event_loop()
    task = loop.create_task(listen())
    print("Magic!")
    await task

if __name__ == '__main__':
    # Change to the "Selector" event loop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Run your async application as usual
    asyncio.run(main())