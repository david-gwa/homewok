# design a nested condition variables in python 



## background 
 the work is derived from [lg-sim/lgsvl/remote](https://github.com/lgsvl/simulator/blob/master-obsolete/Api/lgsvl/remote.py), the original `remote` function is listen message return from server on each `command` request, basically a async request-receive model.
 
 additionaly, we want lg-sim server to send every episode state info to client too, luckily, the server - client communicate is based on `Websocket`，which support server actively pushing message. so simple add a `episode state` info in server side and send it through websocket at every frame works.
 
 
 in `conditional variable` design,  `notify()` won't be hanged-up, while `wait_for()` can be hanged-up if no other thread call `notify()` at first.  
 
 in Python class, to keep object status, it's better to use `class member variable`, rather than `object member variable`, which can't track its status when the object reset. (/)
 
 
 ## try finally
 
 the status update in `try()` package won't be the final status .
 
 
 ```python 
 
 def process(type): 
	status = False 
	try:
		if(type=="a"):
			status = True 
	finally:
		if(type == "b"):
			status = False 
	print("cv.status ....\t", status)
	return status

def main():
	type_list = ["a", "a", "b", "b", "a", "a", "a"];
	for _ in range(len(type_list)):
		print(process(type_list[_]))
 ```
 


## the client design

in client, the message received is handeled in `process()`. by default, there is only one type of message, namely the `event message`, so only one `conditional variable(CV)` is needed to send `notification` to `command()` to actually deal with the recieved message. 

first we defined the new message type(`episode message`), as well as a new real-handel fun `episode_tick()`. then modifying `remote::process()` as:


```python 
try:
	self.event_cv.acquire()    
	self.data = json.loads(data)
	if check_message(self.data) == "episode_message" ：
		self.event_cv.release()
		self.event_cv_released_already = True 
		with self.episode_cv:
			self.episode_cv.notify()
	else :
		self.event_cv.notify()
finally:
	if self.event_cv_released_already:
		self.cv_released_already = False 
	else:
		self.cv.release()

```

## will it dead-locked ?

as both `command()` and `episode_tick()` have conditional variable `wait_for()` :


```python

public command():
	with self.event_cv :
		self.event_cv.wait_for(lambda: self.data is not None)

public episode_tick():
	with self.episode_cv.wait_for(lambda: self.data is not None)
```

so if `notify()` is not called in any situation, `dead-locked` happens, meaning the `wait_for()` will never return but suspended.

`remote.process()` is running in another thread, rather than hte main sim thread, where run `sim.process()`.  `remote.process()` used to accept the message, and `sim.process()` is the actual place to handle these received messages. the two threads run simutaneously.

for any message received, if its type is `event_message`, then it triggers `event_cv.notify()`, so `command()` in `sim::process()` won't dead block;

to avoid `episode_message` dead locked, in `sim::process()` need to call `episode_tick()` only when the message type is `episode_message`, which can be checked by `remote.event_cv_released_already == True`, 


```python 

def sim::process(events):
	j = self.remote.command(events)
	while True:
		if self.remote.event_cv_released_already :
			self.remote.episode_tick()
		if j is None:
			return 
		if "events" in j:
			self._process_events(j)
		
		j = self.remote.command（“continue")
```


			














