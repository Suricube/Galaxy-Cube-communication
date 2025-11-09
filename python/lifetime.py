import asyncio
from typing import Annotated
import aiomqtt
from contextlib import asynccontextmanager
#from fastapi import Depends, FastAPI

async def listen(client):
    async for message in client.messages:
        print(message.payload)

client = None

async def get_mqtt():
    yield client

@asynccontextmanager
async def lifespan():
    global client
    async with aiomqtt.Client("test.mosquitto.org") as c:
        # Make client globally available
        client = c
        # Listen for MQTT messages in (unawaited) asyncio task
        await client.subscribe("humidity/#")
        loop = asyncio.get_event_loop()
        task = loop.create_task(listen(client))
        yield
        # Cancel the task
        task.cancel()
        # Wait for the task to be cancelled
        try:
            await task
        except asyncio.CancelledError:
            pass

#app = FastAPI(lifespan=lifespan)

#@app.get("/")
async def publish(client: Annotated[aiomqtt.Client, get_mqtt]):
    await client.publish("humidity/outside", 0.38)


