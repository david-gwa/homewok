#### C 转行符

[GNU coding standards](https://www.gnu.org/prep/standards/html_node/index.html#SEC_Contents)

[C linux/gnu编程风格](https://www.huihoo.org/gnu/c.html)


#### macro defines 

[C 宏](http://c.biancheng.net/view/446.html)

[C语言中的 __FILE__,  __LINE__, __func__](https://www.cnblogs.com/flyingdirt/p/4237539.html)

[C语言的 __attribute__](https://www.cnblogs.com/flyingdirt/p/4239927.html)

关键字__attribute__ 也可以对结构体（struct ）或共用体（union ）进行属性设置。大致有六个参数值可以被设定，即：aligned, packed, transparent_union, unused, deprecated 和 may_alias 

#### c bit fields

[manipulating bitfields in python](https://jdb.github.io/bitfield.html)

[C - bit fields](https://www.tutorialspoint.com/cprogramming/c_bit_fields.htm)

[C preprocessor, func macro](https://www.tutorialspoint.com/cprogramming/c_preprocessors.htm)


#### volatile 

[C/C++中的volatile](https://zhuanlan.zhihu.com/p/62060524)

 volatile 可以保证对特殊地址的稳定访问





#### C struct assignment 


结构体直接赋值在C语言下是可行


* [函数返回局部变量](https://blog.csdn.net/haiwil/article/details/6691854/)
* [通过参数参数修改实参](https://blog.csdn.net/wallying/article/details/83141860)
* [passing arrays as func arguments in C](https://www.tutorialspoint.com/cprogramming/c_passing_arrays_to_functions.htm)
* [pasing array to func](https://beginnersbook.com/2014/01/c-passing-array-to-function-example/)
* [c数组拷贝](https://www.cnblogs.com/yspworld/p/10749070.html)

```c 
memcpy(dest, src, sizeof(int)*k);
```

#### c struct with another struct array 



[array as member of Structure in C](https://overiq.com/c-programming-101/array-as-member-of-structure-in-c/)

[pointer to an array of structs inside a struct](https://stackoverflow.com/questions/45801808/c-pointer-to-an-array-of-structs-inside-a-struct-within-a-function)


[pointer vs array in C](https://www.geeksforgeeks.org/pointer-vs-array-in-c/)


o sizeof(array) returns the amount of memory used by all elements in array
o sizeof(pointer) only returns the amount of memory used by the pointer variable itself

o &array is an alias for &array[0] and returns the address of the first element in array
o &pointer returns the address of pointer


#### C file IO 

[printf a struct](https://www.linuxquestions.org/questions/programming-9/using-%27printf%27-on-a-%27struct%27-125463/)

* [C 处理太长的换行](https://www.cnblogs.com/3me-linux/p/10302925.html)

* [python按行读取文件，并找出其中指定字符串](https://www.jb51.net/article/167236.htm)




#### C项目结构

* 增量式搭框架，一部分一部分填充，慢慢呈现完成的框。

* 全量式搭框架，最初即是完整的框，慢慢填充内容。 编译配置、代码、单元测试、运行脚本、utils




#### gdb 

* [gdb watch](http://unknownroad.com/rtfm/gdbtut/gdbwatch.html)

* [read watch 2](https://beej.us/guide/bggdb/)

 watch takes an expression as an argument


[gdb catchpoints](https://www.cnblogs.com/arnoldlu/p/13815087.html)


```sh
2       hw watchpoint  keep y                      counter==190
	breakpoint already hit 1 time
3       breakpoint     keep y   0x00007fffe73fe10b exception throw
4       breakpoint     keep y   0x00007fffe73fd3af exception catch
5       catchpoint     keep y                      signal "<standard signals>" 
	catchpoint already hit 3 times

```


[gdb handle命令： 信号处理](http://c.biancheng.net/view/8291.html)


[gdb frame](http://c.biancheng.net/view/8282.html)

```sh

info frame 

info args 

info locals 

```

#### make 

[shell script in one line](https://www.cyberciti.biz/faq/linux-unix-bash-for-loop-one-line-command/)

[shell脚本与makefile的语法区别](https://www.jianshu.com/p/1818a7afe535)

[run make in each subdirectory](https://stackoverflow.com/questions/17834582/run-make-in-each-subdirectory)


[make for compiling: all *.c files in folders and subfolders](https://stackoverflow.com/questions/19539422/make-for-compiling-all-c-files-in-folders-subfolders-in-project)




#### multi c files to one obj

[undefined reference to symbol cos@GLIBC_2.2.5](https://stackoverflow.com/questions/23809404/issue-with-simple-makefile-undefined-reference-to-symbol-cosglibc-2-2-5) 


```
LIBS=-L/usr/lib/x86_64-linux-gnu -lsndfile -lm
```




#### debug compiled obj  


[object files and symbols](http://nickdesaulniers.github.io/blog/2016/08/13/object-files-and-symbols/)


[symbols defined by nm, but undefined by ldd](https://stackoverflow.com/questions/942754/nm-reports-symbol-is-defined-but-ldd-reports-symbol-is-undefined)

[objdump man](https://man.linuxde.net/objdump)

```sh
objdump
readelf
```

#### `ar rcs` 打包静态库 


```sh
ar rcs libshared_utils.a  *.o 
ar t libshared_utils.a #display files in *.a 
gcc -shared -o hwa.so hwa_package.c  -L -lshared_utils
```

#### debug static/dynamic libs 

```sh
nm libshared_utils.a
ldd -r your_lib.so 

```






#### base type 

* [sint32](https://stackoverflow.com/questions/35364786/how-to-printf-a-sint32-in-c-using-gcc-compiler-tricore-v3-4-6)


* [different from int8, int32](https://stackoverflow.com/questions/14515874/difference-between-int32-int-int32-t-int8-and-int8-t)


#### cpu 高占用率100% 卡住

[linux: cpu使用率过高](https://www.jianshu.com/p/6d573e42310a)

```sh
top -p pid
```

#### linux 定时执行任务


[how to schedule tasks/jobs with crontab in Linux](https://www.foxinfotech.in/2019/05/schedule-tasks-jobs-with-cron-crontab-in-linux.html)


[introducing scheduled triggers: API driven cron jobs and scheduled events](https://hasura.io/blog/introducing-scheduled-triggers-api-driven-cron-jobs-scheduled-events/)


#### Signal SIGABRT abort 

* what cause "SIGABRT" ?  

1、double free/free 没有初始化的地址或者错误的地址
2、堆越界
3、assert

对同一个指针free() 2次可能会产生SIGABRT.重复释放内存则会导致sigabrt；


### *** stack smashing detected ***: python3 terminated

```gdb
bt
```

--> stack_chk_fail




[stack_chk_fail debug](https://www.cnblogs.com/zuoanfengxi/p/12610567.html)


[gcc stack-protector]()


[gcc -fstack-protector 检测栈溢出](https://www.cnblogs.com/leo0000/p/5719186.html)

[how to use gcc stack protection](https://stackoverflow.com/questions/1629685/when-and-how-to-use-gccs-stack-protection-feature)

Stack-protection is a hardening strategy, not a debugging strategy. If your game is network-aware or otherwise has data coming from an uncontrolled source, turn it on. If it doesn't have data coming from somewhere uncontrolled, don't turn it on.

For debugging-oriented solutions, look at things like mudflap.


[stack smashing detected 解决过程](https://www.cnblogs.com/wenkyme/p/11988620.html)


[sigsegv, sigabrt, sigbus](https://blog.csdn.net/lby978232/article/details/52712308)


[how to debug sigabrt error](https://mukeshthawani.com/debug-the-sigabrt-error-exception)


[gdb catch](http://c.biancheng.net/view/8199.html)




#### 数据越界


[valgrind debug python memory](https://blog.csdn.net/sishuihuahua/article/details/85930419)


[linux下定位多线程内存越界问题实践](https://zhuanlan.zhihu.com/p/268823073)


[MALLOC_CHECK_ 检查内存问题](https://www.jianshu.com/p/88f6626ed216)


[csdn: stack smashing detected, 程序段错误](https://blog.csdn.net/haidonglin/article/details/53672208)


[stackoverflow: stach smashing detected](https://stackoverflow.com/questions/1345670/stack-smashing-detected)



[a journey into stack smashing](https://lbarman.ch/blog/stack_smashing/)




[what's the use of -fno-stack-protector](https://stackoverflow.com/questions/10712972/what-is-the-use-of-fno-stack-protector)



[gcc build option: -fdelete-null-pointer-checks]()
