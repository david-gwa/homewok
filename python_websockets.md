

## threading.Thread 

## threading api

```shell

run()

start()

join([time])

isAlive()

getName()

setName()

```
to initialize a thread with:  threadID, name, counter



## start() and run()
start() once for each thread, run() will not spawn a separate thread, but run in current thread 

```python 

class myThread(threading.Thread):

	def __init__(self, *args, **kwargs):
		super(myThread, self).__init__(*args, **kwargs)

	def run(self):
		print("run ... from start()")


if __name__ == "__main__":
	demo = myThread()
	demo.start()
	demo.join()

```

## lock objects 

a primitive lock does not belongto a certain thread when locked. by default, when constructed, the lock is in `unlocked` state.


* `acquire()`, will set the lock to `locked` and return the lock immediately(atom operator); if current lock is `locked`, then `acquire()` blocks (the thread) untill the occuping-lock thread calls release().

if multi-thread blocked by `acquire()`, only one thread will get the lock when release() is called, but can't sure which one from the suspended threads



## condition objects 

```shell

threading.Condition(lock=None)

acquire()

wait()

notify()

release()

```

thread A aquire() the condition variable, to check if condition satification, if not, thread A wait; if satisfied, update the condition variable status and notify all other threads in waiting.


[refer](https://cloud.tencent.com/developer/article/1400153)


* initial & destroy

* cond_wait

* cond_notify

*  












