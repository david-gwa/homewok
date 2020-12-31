

##  python ninja 


python has the eco-system to cover all kinds of needs, from data analysis(numpy, pandas), visulization(matplotlib), database, network(websocket, asiohttp), web server, machine learning, xml parser, json serlization, image process, video player, cache middleware, message queue, event system, cross-language(Ctypes) to very special needs, like asammdf only used in auto industry. only can't you image, none can not Python done.

to make a good python project, the first requirement is really familiar with the bussiness logic, the second is really familiar with coding blocks, you know what's there for you, and so can always find these blocks out.

it's also give a way to be master, either you become really specialist in one kind of business, or you become top coder with all kinds of coding blocks and special language candys(e.g. decorator, iterator in Python)

the following is a simple summary to build a python project from 0 to 1, much like something in the book <<high perforamnce python>>


## performance tuning 


* string combination 

```py
i = 1 
str2 = str1 + str(i)
str3 = "%s%s" % (str1, i)
str4 = "str1{}".format(i)
```

* [multi if-else](https://ask.hellobi.com/blog/wangdawei/36646)

* timeit 


* [cython](https://zhuanlan.zhihu.com/p/228594750)


```sh

cp  your.py your.pyx 
vi setup.py 
python setup.py build_ext --inplace 
python -c "import your; your.test()"

```


* memory_profiler 

* liner_profiler 

* [python numba](https://www.cnblogs.com/xihuineng/p/10630116.html)


#### code static check 

* pyflakes 

* pylint

* coverage.py

#### pytest 



#### QA test 

	* pressure test 

	* performance test 


## refer 

[如何建立一个完美的python初始化项目](https://zhuanlan.zhihu.com/p/80078299)

[an overview of profilling tools for python](https://www.blog.pythonlibrary.org/2020/04/14/an-overview-of-profiling-tools-for-python/)

[optimize code using profilers](https://www.jetbrains.com/help/pycharm/profiler.html)

[python性能优化第一步:性能分析实践](https://zhuanlan.zhihu.com/p/24495603)

[python practices for efficient code: memory, usability](https://www.codementor.io/@satwikkansal/python-practices-for-efficient-code-performance-memory-and-usability-aze6oiq65)

[c/c++调用python的一些坑，编译及版本相关](https://www.cnblogs.com/LittleSec/p/10940758.html)

[隐藏源码细节: python编译pyc](https://finthon.com/python-pyc/)

[zhihu: python 性能优化20条建议](https://zhuanlan.zhihu.com/p/41988980)

[zhihu: python 加速运行技巧](https://zhuanlan.zhihu.com/p/143052860)

[cython使用一个setup.py编译多个扩增模块](https://www.jianshu.com/p/abc86ff9fafa)

[snakeviz/runSnakeRun for pstats visualization]()

[python常用代码检查工具](https://www.jianshu.com/p/a61afb09026a)

[python in GO: grumpy](https://github.com/google/grumpy)




		

