
## background 

recently a lot thoughts about design middleware and frameworks in self-driving team. which is a way to go uppper and go more abstract. here specially about `data pipeline` in ADS.

the experience to put lgsvl into swarm/k8s brings the idea about `micro-services`, which is a great way to decouple a large work to a few small pieces of independent but communicatable services. so when coming to handle large data set, which is very common in ADS dev. 

so the first idea is to decouple the `data pipeline` as a few micro-services:  reader service, process service, post-analysis service e.t.c

then two questions immediately up:  which data/message type fits, which network communication protocol fits.and beyond these two basic questions, also need a lot work about message adapter among/in services. previously, I designed `websocket and json` solution. but it's too tedious to plug in a `ws-server/client` at the front/end of each service, especially as the number of serivces grows. 

take it back, `data pipeline` is a heavy data IO work, is it really smart to split the work into a few pieces, then find the network communication among them ? we increase the system complex by introducing additional network communcation moduels, and the only benefit is decouple a heavy data IO work. and more, the network modules need consider cache, job scheduler, load balance issues, as the data process service may take much longer than reader services. 

traditionally, heavy data IO work is common run in `batch processing`, disregarding network issues, and it's better to run directly in memory/cache. so I go to [rq](https://github.com/rq/rq)


## interprocess communication in distributed system

`MPI` is the standard for IPC in HPC apps, of course there are `Linux IPC` libs, which brings more low-level ipc APIs. `MPI` apps mostly run on high performance computing cluster, which has the samilar API e.g. `Allreduce` as `Hadoop/MapReduce`, while the difference `MPI/allReduce` doesn't tolerate failure, which means any node failed, the `MPI` apps failed. Which is the foundmental difference from HPC to distributed system nowadays, really popular as the new infrastructure for cloud and AI. 

in the distributed system, there are a few ways to do interprocess communication:

*  **RESTful protocol**, such as TCP, UDP, websocket. 

* **async communication**, there are different ways to implement async interprocess communication, one way is `message queue`, of course many language, e.g. js, go have some light-weight libs/framework to support ansyc communication interprocessly.

* **rpc**, [thrift]() is an Apache project, [grpc]() is high efficient with protobuf, but it doesn't support well service discovery/load balance mechanism inside, which is a limitation in cloud-native applications.  [dubbo]() has a better design for service discovery and load balance, the message type by default is `json`. so all of these can be the corner-stone service in modern micro service envs. also the common `micro-service framework`, e.g. Spring Cloud has interprocess communication component as well.


for data hungry services, `batch processing` frameworks, e.g. Spring Batch, Linux Parallel should also consider.


## rq 

the following is from [rq doc](http://python-rq.org/docs/)

#### Queues

a `job` is a Python object, namely a function that is invoked async in a worker process. `enqueueing` is simply pushing a reference to the func and its ars onto a queue.

we can add as many Queue instance as we need in one Redis instance, the Queue instance can't tell each other, but they are hosted in the same redis instance, which gives the way to find jobs binding to Queue1 in worker2 from Queue2

#### jobs 


```py 
job1 = q.enqueue(my_func, func_args)
job2 = Job.create(my_func, ttl=100, failure_ttl=10, depends_on=, description=, func_args)
q.enqueue_job(job2)
```

* timeout: specifies the max runtime of job before it's interrupted and marked as failed. 
* ttl: specifies the maximum queued time(in sec) of the job before it's dscarded. default is None(infinite TTL)
* failure_ttl: specifies how long(in sec) failed jobs are kept(default to 1 years)

the following sample is a way to find all `rq:job:`s, but the return is a bytes object, which need encode as `utf-8` for any further usage.

```py 
import redis
r = redis.StrictRedis()
r.keys()
for key in r.scan_iter("rq:job:*"):
	print(key.encode('utf-8')

```


#### workers

workers will read jobs from the given queues(the order is important) in an endless loop, waiting for new work to arrive when all jobs done. each worker will process a single job at a time. by default, workers will start working immediately and wait until new jobs. another mode is `burst`, where to finish all currently avaiable work and quit asa all given queues are emptied.

`rq worker` shell script is a simple `fetch-fork-execute` loop
 
## connections

when you want to use multiple connections, you should use `Connection` contexts or pass connections around explicitly. 


```py
conn1 = Redis('localhost', 6379)
conn2 = Redis('remote.host.org', 9836)

q1 = Queue('foo', connection=conn1)
q2 = Queue('bar', connection=conn2)
```

Every job that is enqueued on a queue will know what connection it belongs to. The same goes for the workers. 
within the Connection context, every newly created RQ object instance will have the connection argument set implicitly.

```py
    def setUp(self):
        push_connection(Redis())

    def tearDown(self):
        pop_connection()
```

this should be the way to handle distributed queues. 


#### results

if a job returns a `non-None` value, the worker will write that return value back to the job's Redis hash under `result` key. the job's Redis hash itself expire in 500sec by default after the job is finished.


```py
q.enqueue(foo, result_ttl=86400)  # result expires after 1 day
q.enqueue(func_without_rv, result_ttl=500)  # job kept explicitly
```

when an exception is thrown inside a job, it's caught by the worker, serialized and stored under `exc_info` key. By default, jobs should execute within 180 seconds. After that, the worker kills the work horse and puts the job onto the failed queue, indicating the job timed out.

```py
q.enqueue(mytask, args=(foo,), kwargs={'bar': qux}, job_timeout=600)  # 10 mins
```


#### job registries 

each queue maintains a set of Job Registries. e.g.  `StartedJobRegistry`, `FinishedJobRegistry` e.t.c. we can find these after log in `redis-cli`


#### version bug 

when run `rq` demo, it reports: 

```python
raise RedisError("ZADD requires an equal number of "
redis.exceptions.RedisError: ZADD requires an equal number of values and scores
```

manually change `/rq/registry.py`:

```py
 # return pipeline.zadd(self.key, {job.id: score})
return pipeline.zadd(self.key, job.id, score)
```

## redisgn data pipeline

* queues 

```python
conn = Redis() 
mf4q = Queue('mf4Q', connection=conn)
aebq = Queue('aebQ', connection=conn)
dbq = Queue('dbQ', connection=conn)
```


* jobs

```python
def mf4_jober(url_path):
    mf4_job = mf4q.enqueue(mf4_reader, args=(url_path,), timeout=60, ttl=60, failure_ttl=1,  job_timeout=60, result_ttl=60, job_id=mf4_job_id)

def aeb_jober(mf4_frames):
    aeb_job = aebq.enqueue(aeb_oneStep, args=(i_, ), timeout=60, ttl=20, failure_ttl=1, result_ttl=10, job_id=aeb_job_id)
	
def db_jober(aeb_frame, idx):
    db_job= dbq.enqueue(db_oneStep, args=(aeb_frame,), timeout=60, ttl=20, failure_ttl=1, job_id=db_job_id) 
```


* workers 

```python

def mf4_workers(conn, num_workers=1):
	for i in range(num_workers):
		worker_ = Worker([mf4q], connection=conn, name=worker_name)
		workers_.append(worker_)
	for w in workers_:
		w.work(burst=True)

def aeb_workers()

def db_workers()


```


* runners

```py 
def runner(conn):
	mf4_workers(conn)
	for k in conn.scan_iter("rq:job:mf4_job_*"):
		t_ = k.decode('utf-8')
		j_ = Job.fetch(t_[7:], connection=conn)
		aeb_jober(j_.result)
	input("hold on ...")
	aeb_workers(conn)
```

since the output of `mf4` jobs is the input of `aeb`, so we need `runners`, similar for `db`.


## summary 

 `rq` is a good framework for this level data pipleine. for even bigger and complex system, `rq` maybe just a middleware, and there should be an even larger framework. the software engineering idea about `framework` and `middleware` in a large system gradually become the foundataion of ADS team


## refer

[xiaorui blog: rq](http://xiaorui.cc/)

[微服架构中的进程间通信](https://www.cnblogs.com/jpwahaha/p/10601096.html)

[微服务架构](https://www.cnblogs.com/imyalost/p/6792724.html)

[使用gRPC构建微服务](https://www.tuicool.com/articles/QreqUnU)

[微服务, 通信协议对比](https://blog.csdn.net/fly910905/article/details/100016003)

[理解批处理的关键设计](https://cloud.tencent.com/developer/article/1081697)

[spring batch 批处理](https://www.cnblogs.com/rookiemzl/p/9788002.html)




