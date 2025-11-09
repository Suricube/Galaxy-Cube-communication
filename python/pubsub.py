import asyncio
import aiomqtt

loop = asyncio.get_event_loop()

async def demo():
    c = aiomqtt.Client(loop)
#    c.loop_start()  # See "About that loop..." below.

    connected = asyncio.Event()
    def on_connect(client, userdata, flags, rc):
        connected.set()
    c.on_connect = on_connect

    await c.connect("localhost")
    await connected.wait()
    print("Connected!")

    subscribed = asyncio.Event()
    def on_subscribe(client, userdata, mid, granted_qos):
        subscribed.set()
    c.on_subscribe = on_subscribe

    c.subscribe("my/test/path")
    await subscribed.wait()
    print("Subscribed to my/test/path")

    def on_message(client, userdata, message):
        print("Got message:", message.topic, message.payload)
    c.on_message = on_message

    message_info = c.publish("my/test/path", "Hello, world")
    await message_info.wait_for_publish()
    print("Message published!")

    await asyncio.sleep(1)
    print("Disconnecting...")

    disconnected = asyncio.Event()
    def on_disconnect(client, userdata, rc):
        disconnected.set()
    c.on_disconnect = on_disconnect

    c.disconnect()
    await disconnected.wait()
    print("Disconnected")

    await c.loop_stop()
    print("MQTT loop stopped!")

loop.run_until_complete(demo())
