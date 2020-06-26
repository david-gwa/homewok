
## setup

[install boost](https://www.boost.org/doc/libs/1_73_0/more/getting_started/unix-variants.html)

[configuring Boost.BUild](https://www.boost.org/doc/libs/1_72_0/libs/python/doc/html/building/configuring_boost_build.html)

python env :  3.6 (from conda env aeb) 
gcc:  4.5.0 

```sh
export BOOST_BUILD_PATH=`pwd`   #where we keep `user-config.jam`
```

#### user-config.jam

```yml
using gcc : 5.4.0 : /usr/bin/g++ ;

using python : 3.6
        : "/home/anaconda3/envs/aeb/bin/python"
        : "/home/anaconda3/envs/aeb/include"
        : "/home/anaconda3/envs/aeb/include/python3.6m" ; 
``` 

bootstrap will find `user-config.jam` from $BOOST_BUILD_PATH. 

```sh 
cd  /path/to/boost_1_73_0
./bootstrap.sh --help
./bootstrap.sh --prefix=/usr/local/ --show-libraries
b2 --with-python --prefix="/usr/local/" install variant=release link=static address-model=64 
b2 --clean
```

[a sample of user-config.jam](https://cloud.tencent.com/developer/article/1011767)

* error fixing 

```sh 
fatal error: pyconfig.h: No such file or directory
compilation terminated.
```

need `export CPATH=~/anaconda/envs/aeb/include/python3.6m/`,  where located `pyconfig.h` and other headers

finally report:

```sh
...updating 15 targets...
common.copy /usr/local/lib/libboost_numpy36.so.1.73.0
common.copy /usr/local/lib/libboost_python36.so.1.73.0
common.copy /usr/local/lib/cmake/boost_python-1.73.0/libboost_python-variant-shared-py3.6.cmake
common.copy /usr/local/lib/cmake/boost_numpy-1.73.0/libboost_numpy-variant-static-py3.6.cmake
common.copy /usr/local/lib/cmake/boost_numpy-1.73.0/libboost_numpy-variant-shared-py3.6.cmake
common.copy /usr/local/lib/libboost_numpy36.a
common.copy /usr/local/lib/cmake/boost_python-1.73.0/libboost_python-variant-static-py3.6.cmake
common.copy /usr/local/lib/cmake/Boost-1.73.0/BoostConfigVersion.cmake
ln-UNIX /usr/local/lib/libboost_numpy36.so
common.copy /usr/local/lib/libboost_python36.a
ln-UNIX /usr/local/lib/libboost_python36.so
ln-UNIX /usr/local/lib/libboost_numpy36.so.1
ln-UNIX /usr/local/lib/libboost_python36.so.1
ln-UNIX /usr/local/lib/libboost_numpy36.so.1.73
ln-UNIX /usr/local/lib/libboost_python36.so.1.73
``` 

boost.python build successfully !


## demo run

the following is simple sample of how to use boost_python wrapper to wrapping an AEB model(in c++) to python

####  aeb.h 

```c++
#include <iostream>
#include <string>


typedef struct {
	float time; 
	float dx ;
	float dy ;
} AEB;

typedef struct {
	AEB out1 ;
} OP;



class aeb {
    public:
        Student() {}
	OP op_out ;
        void test_op(){
            (void) memset((void *)&op_out, 0, sizeof(OP)); 
            op_out.out1.time = 1.0 ; 
            op_out.out1.dx = 2.0 ;
            op_out.out1.dy = 3.0 ; 
            AEB o1 = op_out.out1 ;
            std::cout << o1.time << std::endl ;
        }
};

```

#### wrap_student.cpp

```c++
#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "aeb.h"

using namespace boost::python;

BOOST_PYTHON_MODULE(aeb) {
    scope().attr("__version__") = "1.0.0";
    scope().attr("__doc__") = "a demo module to use boost_python.";
    class_<aeb>("aeb", "a class of aeb")
        .def(init<>())
        .def("test_op", &aeb::test_op, "test op")
        .def_readonly("op_out", &aeb::op_out)
}
``` 

tips, to using nested structure in wrapper is another topic later.

#### build and python import 

* check header location

      Python.h @ `/home/anaconda3/envs/aeb/include/python3.6m`

      boost/python @ `/usr/local/include/boost`

* check *.so lib location
     
       /usr/local/lib/


tips, if there is duplicated `boost lib` in system, e.g. `/usr/lib/x86_64-linxu-gnu/libboost_python.so` which maybe conflict with `boost_python` install location at `/usr/local/lib/libboost_python36.so`

* build 

```sh
g++ -I/home/anaconda3/envs/aeb/include/python3.6m -I/usr/local/include/boost -fPIC wrap_student.cpp -L/usr/local/lib/ -lboost_python36 -shared -o student.so
```

* test 

```python
import aeb
aeb.test_op(2, 5.1)      
```




#### refere

[boost.python tutorial](https://www.boost.org/doc/libs/1_66_0/libs/python/doc/html/tutorial/index.html)



