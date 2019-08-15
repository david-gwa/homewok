import asyncio 
from threading import Thread 

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def thread_(name):
    print("executing name:", name)
    return "return nam:" + name 

_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(_loop,)) #is a thread or coroutine ?
t.start()


handle = _loop.call_soon_threadsafe(thread_, "zj")
handle.cancel()

_loop.call_soon_threadsafe(thread_, "zj2")

print("main thread non blocking...")


_loop.call_soon_threadsafe(thread_, "zj3")

print("main thread on going...")




