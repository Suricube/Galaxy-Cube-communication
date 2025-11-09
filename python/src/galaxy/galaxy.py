''' general galaxy class'''
from enum import Enum
from .component import Component
from asyncio import Future
from asyncio import AbstractEventLoop
import asyncio
from gmqtt import Client as MQTTClient
import time
import json

active_galaxy_msgs = {}

async def add_to_list(my_future):
    print('adding future to active_future_list')
    active_galaxy_msgs["test"]=my_future


def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('galaxy', qos=0)

def on_message(client, topic, payload, qos, properties):
    print('RECV MSG:', payload.decode(), 'on topic:', topic)
    msg = payload.decode()
    value = json.loads(msg)
    id = value.get("id")
    if  id is not None:
        fut = active_galaxy_msgs.get("test", None)
        if fut is not None: 
            print("found future")
            fut.set_result(msg)
            active_galaxy_msgs.pop("test")

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')

class Galaxy:
    def __init__(self, loop: AbstractEventLoop, ip: str, topic: str):
        self.ip    = ip
        self.topic = topic
        self._loop = loop

        self.c = MQTTClient("gmqtt-client")

        self.c.on_connect = on_connect
        self.c.on_message = on_message
        self.c.on_disconnect = on_disconnect
        self.c.on_subscribe = on_subscribe

    async def connect(self):
        await self.c.connect("localhost")

    def send(self, comp: Component)-> Future:
        self.c.publish('ui', comp.to_msg(), qos=1,content_type='utf-8', user_property=('timestamp', str(time.time())))
        my_future = Future()
        self._loop.create_task(add_to_list(my_future))
        return my_future

