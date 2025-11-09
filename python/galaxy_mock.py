''' a mock emulating the Galaxy controller '''
import asyncio
import aiomqtt
import json
import uuid

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
            id = 123
            comp_id = 234
            print("msg")
            print("msg: "+message.payload.decode("utf-8"))
            value = json.loads(message.payload.decode("utf-8"))
            cmd = value["command"]
            print(cmd)
            msg = {}
            match cmd:
                case "system":
                    name = value["component_tasks"][0]["component_cmd"]
                    print(name)
                    match name:
                        case "capabilities":
                            caps = [ob.to_dict() for ob in capabilities]
                            msg = {
                                "component_name":name,
                                "msg_id": id,
                                "component_id": comp_id,
                                "capabilities":caps,
                            }
                        case _:
                            msg = {"error":"wrong command"}

                case "component":
                    name = value["tasks"][0]["component_name"]
                    print(name)
                    id = 1234
                    comp_id=1234
                    msg = {
                        "component_name":name,
                        "msg_id": id,
                        "component_id": comp_id
                    }
                case _:
                    msg = {"error":"wrong command"}
            print(json.dumps(msg))
            await client.publish("galaxy",payload=json.dumps(msg))

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