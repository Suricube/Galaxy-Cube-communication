''' general galaxy class'''
from enum import Enum
from .component import Component
from asyncio import Future
from asyncio import AbstractEventLoop
import asyncio


class Galaxy:
    def __init__(self, loop: AbstractEventLoop, ip: str, topic: str):
        self.ip    = ip
        self.topic = topic
        self._loop = loop


