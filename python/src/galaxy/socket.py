import asyncio
import aiomqtt
from asyncio import Future
from asyncio import AbstractEventLoop
from gmqtt import Client as MQTTClient
import json
from result import Ok, Err, Result, is_ok, is_err

# singleton
active_galaxy_msgs = {}

async def add_to_list(id, my_future, callback):
    if id is not None:
        print('adding future to active_future_list')
        active_galaxy_msgs[id]={"fut": my_future, "callback":callback}


class GalaxySocket:
    def __init__(self, loop: AbstractEventLoop):
        self._loop = loop

    def send():
        pass
    def sendawait(self, msg: str, callback)-> Future:
        value = json.loads(msg)
        id = value.get("tasks",{})[0].get("payload",{}).get("reply",{}).get("msg_id")
        my_future = Future()
        # register future and callback in active reply list before sending message
        if id is not None:  # if uuid exists keep track of id for async reply message
            print(id)
            self._loop.create_task(add_to_list(id, my_future, callback))
        else:               # no id, don't wait for reply message, future finishes directly
            self._loop.create_task(add_to_list(id, my_future, callback))
            my_future.set_result(None)
        # send message, potentially need to check if executed correctly here
        self.send(msg)
        return my_future
    
    def parse_message(msg: str):
        pass

# MQTT implementation of GalaxySocket

class GalaxyMQTT(GalaxySocket):
    def __init__(self, loop: AbstractEventLoop, ip: str, port: int):
        GalaxySocket.__init__(self, loop)
        print("start client to MQTT")
        self.ip = ip
        self.port = port
        self.c = MQTTClient("galaxy-client")
        self.c.on_connect = self.on_connect
        self.c.on_message = self.on_message
        self.c.on_disconnect = self.on_disconnect
        self.c.on_subscribe = self.on_subscribe

    async def connect(self):
        await self.c.connect(self.ip)

    def send(self, msg: str):
        self.c.publish('ui', msg, qos=1,content_type='utf-8')

    def on_connect(self, client, flags, rc, properties):
        print('Connected')
        client.subscribe('galaxy', qos=0)

    def on_message(self, client, topic, payload, qos, properties):
        msg = payload.decode()
        print('RECV MSG:', msg, 'on topic:', topic)
        self.parse_message(msg)

    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_subscribe(self, client, mid, qos, properties):
        print('SUBSCRIBED')

    def parse_message(self, msg: str):
        value = json.loads(msg)
        id = value.get("msg_id")       # msg needs to have an id
        payload = value.get("payload") # msg needs to have a payload
        if  id is not None and payload is not None:
            print("found id and payload")
            futcb = active_galaxy_msgs.get(id, None)
            if futcb is not None:
                fut = futcb.get("fut")
                cb = futcb.get("callback")
                print("found future and callback")
                result = cb(payload) # process payload by component callback
                fut.set_result(result)
                active_galaxy_msgs.pop(id)

# Websocket implementation of GalaxySocket

class GalaxyWS(GalaxySocket):
    def __init__(self, loop: AbstractEventLoop, ip: str, port: int):
        GalaxySocket.__init__(self, loop)
        print("start client to MQTT")
        self.ip = ip
        self.port = port
