

## python 分析器


[grumpy](https://github.com/google/grumpy)

[python性能优化技巧](https://www.cnblogs.com/lisongzzx/p/13729187.html)


[an overview of profilling tools for python](https://www.blog.pythonlibrary.org/2020/04/14/an-overview-of-profiling-tools-for-python/)




[the python profilers](https://cloud.tencent.com/developer/section/1367501)

[profile and pstats sample](https://blog.51cto.com/tongcheng/1770508)

## line profiler


## memory profiler 

[zhihu: memory profiler](https://zhuanlan.zhihu.com/p/121003986)

[python内存监测](https://www.cnblogs.com/kaituorensheng/p/5669861.html)




## cython 


[用cython加速python到起飞](https://www.jianshu.com/p/fc5025094912)

[.py 与 .pxd文件的区别](https://cloud.tencent.com/developer/article/1524924)



## pyCharm 

[optimize code using profilers](https://www.jetbrains.com/help/pycharm/profiler.html)


## cProfile 


## [python性能优化第一步:性能分析实践](https://zhuanlan.zhihu.com/p/24495603)


* install [runSnakeRun](https://www.pixelstech.net/article/1599647177-Problem-and-Solution-for-Installing-wxPython-on-Ubuntu-20-04)


```sh
sudo apt-get install libgtk-3-dev
#sudo apt-get install libglib2.0-dev
sudo apt-get install python-wxtools
#sudo apt-get install runsnakerun  --> runsnake
pip3 install RunSnakeRun 
```


[ubuntu安装wxPython](https://www.jianshu.com/p/1429751caa5b)


[ubuntu安装wxpython](https://m.linuxidc.com/Linux/2012-11/73911.htm)


[instlal wxPython on ubuntu](https://www.pixelstech.net/article/1599647177-Problem-and-Solution-for-Installing-wxPython-on-Ubuntu-20-04)



[runSnakeRun for py2.7](http://www.vrplumber.com/programming/runsnakerun/)



## xwpython build error 


```sh
err: g++: error: unrecognized command line option ‘-fno-plt’
```


[fix1](https://github.com/argman/EAST/issues/233)


```sh
python3-config --cflags

```


[c/c++调用python的一些坑，编译及版本相关](https://www.cnblogs.com/LittleSec/p/10940758.html)



**runSankeRun in python3.6 failed.**


## snakeviz

```sh
pip3 install snakeviz
 snakeviz get_dfs.prof 
```


[python practices for efficient code: memory, usability](https://www.codementor.io/@satwikkansal/python-practices-for-efficient-code-performance-memory-and-usability-aze6oiq65)





## python  numba


[一行代码让python提速100倍](https://www.cnblogs.com/xihuineng/p/10630116.html)


test with numba


```sh
get_5r1v_pack() avg time: 0.035379225285209, and total time: 7.040465831756592
avg get_v71_vcan_pack time: 0.0037047827064092434, and total time: 0.7372517585754395
C run total time 0.03179287910461426
for loop total time: 9.112128734588623
运行总时间: 17.14309859275818

get_5r1v_pack() avg time: 0.03585474814601879, and total time: 7.135094881057739
avg get_v71_vcan_pack time: 0.003757631359387882, and total time: 0.7477686405181885
C run total time 0.0326235294342041
for loop total time: 9.278679847717285
运行总时间: 17.41678547859192

```


even slower than without numba







## pyc 文件


[隐藏源码细节: python编译pyc](https://finthon.com/python-pyc/)





[python 性能优化](https://www.cnblogs.com/xybaby/p/6510941.html)


[zhihu: python 性能优化20条建议](https://zhuanlan.zhihu.com/p/41988980)

[zhihu: python 加速运行技巧](https://zhuanlan.zhihu.com/p/143052860)


## cython


[zhihu: 使用cython来加上python](https://zhuanlan.zhihu.com/p/228594750)


```sh

cp  your.py your.pyx 

vi setup.py 

python setup.py build_ext --inplace 

python -c "import your; your.test()"

```


[cython使用一个setup.py编译多个扩增模块](https://www.jianshu.com/p/abc86ff9fafa)




#### cython build errors 


[尝试利用Cython将python项目转换成.so](https://paper.seebug.org/1139/)





## python code check 



#### 代码检查

[python常用代码检查工具](https://www.jianshu.com/p/a61afb09026a)


* pyflakes 

* pylint


#### 自动化测试

[pytest](https://zhuanlan.zhihu.com/p/63155927)





#### 覆盖检测

[coverage.py]()






