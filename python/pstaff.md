

#### python class attributes 

Python classes and instances of classes each have their own distinct namespaces represented by pre-defined attributes `MyClass.__dict__` and `instance_of_MyClass.__dict__` , respectively. check [python class attributes: an overly through guide](https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide)


check attributes in an instance: 

```py
dir(type(self))
type(self).__dict__

self.__getattribute__()
self.__setattr__()
```

####  python instance equality 

```sh
    is is used to compare identity
    == is used to compare equality
```

check [compare object instances for equality by their attributes](https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes)



#### python object to json 

[unable to serialize nested python object using json.dumps](https://stackoverflow.com/questions/63675201/unable-to-serialize-a-nested-python-object-using-json-dumps)

[serializing instance to json](https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json)


`isintance()` can consider derived class, while `type()` can't 

#### size of python object


[difference between __sizeof__ and sys.getsizeof](https://www.geeksforgeeks.org/difference-between-__sizeof__-and-getsizeof-method-python/)

`getsizeof()` method calls `__sizeof__()` method of the object with an additional garbage collector overhead. 


[ctypes.sizeof vs  sys.getsizeof](https://stackoverflow.com/questions/27213647/ctypes-in-python-size-with-the-sys-getsizeofvar-method-vs-ctypes-sizeofvar)


`ctypes.sizeof()` return the actual size of `C` data type that is within the Python object(using C's `sizeof` operator); a macro `PyObject_HEAD` is attached to the start of every object. This increases the size of the Python object. `sys.getsizeof` gets the size of that Python object, which is larger than the corresponding object in C.


[finding the size of python objects](https://www.scrygroup.com/tutorial/2018-09-04/find-size-of-python-object/)

```py
import sys 
from ctypes import c_float, sizeof

c1 = c_float(1.0)
c2 = 1.0
c1.__sizeof__()  #112 
sys.getsizeof(c1) #136 
sizeof(c1)  # 4
c2.__sizeof__() #24
sys.getsizeof(c2) #24
```

#### python list to c array 


* python array vs list 


python array can only used for basic types, and it need declaration first.


[convert python list to C array](https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes)

```py
import ctypes
pyarr = [1, 2, 3, 4]
arr = (ctypes.c_int * len(pyarr))(*pyarr)
```


#### python virtual env out-of-memory

```sh
Sep 14 08:22:10 ubuntu kernel: Killed process 10764 (python3) total-vm:14188800kB, anon-rss:13541608kB, file-rss:0kB, shmem-rss:0kB
```

[Linux Out-Of-Memory killer](https://rdc.hundsun.com/portal/article/748.html)


#### python file io

```sh
AttributeError: '_io.TextIOWrapper' object has no attribute 'next'

```

[fileinput](https://www.jb51.net/article/177680.htm)


python3 File 对象 不支持  file.next()
 


#### python gdb 

[gdb --args](https://www.cnblogs.com/justinzhang/p/9282334.html)

```sh
gdb --args python-dbg main.py
```

[gdb python](https://m.linuxidc.com/Linux/2017-11/148329.htm)

it's the case when need to gdb python-C libs together. 

```sh
gdb python
b your_C_func
run main.py
```

#### ctypes 


*  [default values in ctypes Structure](https://stackoverflow.com/questions/7946519/default-values-in-a-ctypes-structure)


* [ctypes struct pointer](https://bytes.com/topic/python/answers/801681-ctypes-return-pointer-struct)


## pandas 


#### dataframe 

[pandasgui](https://github.com/adamerose/pandasgui)
 
[append Series to rows of df wthout making a list](https://stackoverflow.com/questions/33094056/is-it-possible-to-append-series-to-rows-of-dataframe-without-making-a-list-first)


#### python module performance test 

[line_profiler](https://github.com/rkern/line_profiler)

[memory_profiler]()



#### concurrent 

* [concurrent.futures](https://pymotw.com/3/concurrent.futures/)

* [python Queue](https://www.jianshu.com/p/e30d302ebdeb)


```py
ts_iter = map(lambda x: int((x + self.base_time) * 1e6), df.index)
```

[python map, lambda](https://zhuanlan.zhihu.com/p/133679417)

[pandas groupBy 技术](https://www.cnblogs.com/huiyang865/p/5577772.html)


#### aiohttp



[asyncio]()

[itertools]()



#### 网络测试工具

[speedtest-cn-cli](https://www.speedtest.cn/cli)

[网速测试工具](https://linux.cn/article-11882-1.html)

[wrk web服务器压力测试](https://www.cnblogs.com/woshimrf/p/wrk.html)



#### python green event

[gevent](http://www.gevent.org/)


[monkey patch](https://cloud.tencent.com/developer/article/1441252)


[libevent](https://segmentfault.com/blog/amc?tag=libevent)

[libhv](https://github.com/ithewei/libhv)

[backend: libevent](https://segmentfault.com/blog/amc?tag=libevent)

[huey: event scheduler in python](https://github.com/coleifer/huey)

[gevent: greenevent in python](https://github.com/gevent/gevent)



[does multithreading make sense for IO-bound](https://stackoverflow.com/questions/902425/does-multithreading-make-sense-for-io-bound-operations)

#### python file operation

[python glob](https://www.cnblogs.com/huangm1314/p/11318514.html)



