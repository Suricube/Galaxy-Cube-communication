import sys
from src.galaxy import *
from asyncio import Future
import asyncio
import json
import time
import signal

from gmqtt import Client as MQTTClient




STOP = asyncio.Event()



def ask_exit(*args):
    STOP.set()


async def main(loop) -> int:

    # = asyncio.get_event_loop()

    sag0 = SAG("ASG0")
    sag0.set_properties(SecRepetions.continuous)
    sec  = SectionAO(0.,1.,0.,0.,10,SecTimeUnits.ms,SecOrder.linear)
    sag0.append_section(sec)

    g = Galaxy(loop, "localhost","galaxy")
    await g.connect()

    print(sag0.to_msg())
    f = g.send(sag0)
    result = await f
    print(result)

    print("after send!")

    await STOP.wait()
    await g.disconnect()

    time.sleep(5)

    print("Done!")

#    f1 = g.launch("ASG_0","wasmfile") # instantiate ASG_0
#    f2 = g.launch("ASG_1","wasmfile")
#    f3 = g.launch("ASG_2","wasmfile")
#    join(f1,f2,f3) # wait until all done
#    checkiferror # success?
#    f1= g.task(sag0.set()).await.unwrap() # set sections
#    f2= g.task(sag1.set()).await.unwrap() # set sections
#    joins(f1,f2) #wait for both 
#    g.taks(sag1.run()).await
#    g.taks(sag1.close()).await

    return 0

if __name__ == '__main__':
    # Change to the "Selector" event loop
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Run your async application as usual
#    asyncio.run(main())

    loop = asyncio.get_event_loop()
    
    # Add signal handlers for graceful shutdown
    #loop.add_signal_handler(signal.SIGINT, ask_exit)
    #loop.add_signal_handler(signal.SIGTERM, ask_exit)
    
    loop.run_until_complete(main(loop))