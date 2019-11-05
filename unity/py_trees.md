## background 

behavior trees(BT) are a decision making engine, others include hierarchical finite state machines, task networks.

## composites 

* sequence,  execute children sequentially

* selector 

* chooser 

* parallel, manage children concurrently  


### Sequence 

 	py_trees.composites.Sequence(name='Seqence', children=None)

A Sequence will progressively tick over each of its children so long as each child returns `SUCCESS`, if any child returns `FAILURE` or `RUNNING`, the sequence will halt and the parent will adopt the result of this child 


### Parallel 
	
	py_trees.composites.Parallel(name:, policy: children:)
 
tick every child every time the parallel is run.

Parallels with policy `SuccessOnOne` return `SUCCESS` if at least one child returns `SUCCESS` and others are `RUNNING` 


## 

py_trees API

### py_trees.behaviour 

```python 
	py_trees.behaviour.Behaviour(name) 	
        iterate() #to traverse the entire tree 
   	tick() #used by an iterator on an entire behaviour tree, it handles the logic to call initialise(), terminate() and the actuall update() method, which determines the behaviour's new status once the tick has finished

	tick_once()

	update() 

	
all behaviours, standalone and composite, inheirt from this class.

 
### py_trees.common 

```python

   py_trees.common.ParallelPolicy() 

   py_trees.common.Status()

   py_trees.common.ClearingPolicy() 

```

### py_trees.composites 

manage children and apply some logic to the way they execute and return a result, 


```python

	py_trees.composites.Parallel
	py_trees.composites.Sequence
	py_trees.composites.Selector
	
```	

#### py_trees.composites.Parallel

```python
	setup() #
	tick() # tick over children
```

	
#### py_trees.composites.Selector

```python

	stop()
	tick() # 
```

### py_trees.meta 






















 
