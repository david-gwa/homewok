
## iterator protocol 

* iterator object should have next() method, to return next object or StopIteration Error

* iteratable object, the object that can be iterator 

* protocol


## generator 

to support delay operations, only return result when need, but not immediately return


* generator funcion (with `yield`) 

* generator expression 


Python generator in other languages is calld `coroutines` 


## coroutines 

```python
def cor1(name):
        print("start cor1..name..", name)
        x = yield name
        print("send value", x)

cor_ =  cor1("zj")
print("next return", next(cor_))
print("send return", cor_.send(6))
```

to run coroutine, need first call next(), then send() is called. namely, if not call next() first, send() will wait, and never be called.

the thing is, when define a python generator/coroutine, it never will run; only through await(), next() call first, which then trigger the generator/coroutine start.

 

## asyncio 

asyncronized IO, event-driven coroutine, so users can add `async/await` to time-consuming IO.


* event-loop

event loop will always run, track events and enqueue them, when idle dequeue event and  call event-handling() to deal with it.


* asyncio.Task


## await 

await only decorate async/coroutine, which is a waitable object, it works to hold the current coroutine(async func A) and wait the other coroutine(async func B) to the end.

```shell

async def funcB():
	return 1

async def funcA():
	result = await funcB()
        return result

run(funcA())

```



## multi-task coroutines

```shell

loop.create_task()

run_until_complete() #block the thread untill coroutine completed

asyncio.sleep() #nonblock event-loop, with `await`, will return the control-priority to event-loop, at the end of sleep, control-priority will back to this coroutine 

asyncio.wait(), #nonblock event-loop, immeditialy return coroutine object, and add this corutine object to event-loop

``` 

the following example:  get the event-loop thread, add coroutine objct(task) in this event-loop, execute task till end.

```python

import asyncio

async def cor1(name):
        print("executing: ", name)
        await asyncio.sleep(1)
        print("executed: ", name)

loop = asyncio.get_event_loop()
tasks = [cor1("zj_" + str(i)) for i in range(3)]
wait_cor = asyncio.wait(tasks)
loop.run_until_complete(wait_cor)
loop.close()

``` 

## dynamically add coroutine


```shell 

loop.call_soon_threadsafe() # add coroutines sequencially  
asyncio.run_coroutine_threadsafe() #add coroutines async 
```

### add coroutine sequencially 

in this sample, main_thread(_loop) will sequencely run from begining to end, during running, there are two coroutines registered, when thread-safe, these two coroutines will be executed.

the whole process actually looks like run in sequencialy


```python
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

```


### add coroutines async

in this way, add/register async coroutine objects to the event-loop and execute the coroutines when thead-safe

```python
future = asyncio.run_coroutine_threadsafe(thread_("zj"), _loop)
print(future.result())

asyncio.run_coroutine_threadsafe(thread_("zj2"), _loop)

print("main thread non blocking...")


asyncio.run_coroutine_threadsafe(thread_("zj3"), _loop)

print("main thread on going...")

```


### producer-consumer model in coroutines 

[refer](https://zhuanlan.zhihu.com/p/59621713)
















