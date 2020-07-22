
## background 

more engineering works in practical projects when using boost.python to modulized C++ projects. 

* how to use private variables 

* how to call private methods

* how to use raw functions

e.t.c 


## C++ class with private variables to boost.python

#### a.hpp

```hpp
#include <iostream>

class AA{
	public:
		AA();
		AA(int n);
		int printA() ; 
		void setA(int nn);
		void ptest_public(); // a public wrapper to private method
	private:
		int number_ ;
		void ptest();
};

```

#### a.cpp 

```cpp
#include "a.hpp"
		AA::AA(){}
		AA::AA(int n){number_ = n ; }
		int AA::printA(){ return number_; }
		void AA::setA(int nn){this->number_ = nn ; }
		void AA:ptest(){std::cout << "I am private method in AA" << std::endl ;}
		void AA::pptest(){ ptest();}
```

#### wrapper_a.cpp

```cpp
#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/data_members.hpp>
#include <boost/python/module.hpp>
#include <boost/python/class.hpp>

#include "a.hpp"

using namespace boost::python;

BOOST_PYTHON_MODULE(aa) {	
	class_<AA>("AA", " a class of AA")
		.def(init<>())
		.def(init<int>())
		// .def("get", make_getter(&AA::number_))
		// .def("set", make_setter(&AA::number_))
		//.add_property("member_", make_getter(&AA::number_))
		.def("printA", &AA::printA) 
		.def("setA", &AA::setA)
		.add_property("number_", &AA::printA, &AA::setA)  // take care the order of getter and setter
		.def("ptest_pub", &AA::pptest)	
	;
}
```


#### build

```sh
 g++ -I/home/anaconda3/envs/aeb/include/python3.6m -I/usr/local/include/boost -fPIC wrapper_a.cpp a.cpp -L/usr/local/lib/ -lboost_python36 -shared -o aa.so 

```

#### test 

```python
import aa
a1 = aa.AA(10)
aa.number_
```


#### C++ class with private method to boost.python

as the sample above, a common way to use private method from C++, is to define a public wrapper func, inside which call the private method. 

another way is go to [boost.bind](https://www.boost.org/doc/libs/1_64_0/libs/bind/doc/html/bind.html), where any member functions can be called via a pointer-to-member-function, [regardless of its accessibility](https://stackoverflow.com/questions/6538133/how-can-boostbind-call-private-methods). 




#### add_property

[add_property](https://www.boost.org/doc/libs/1_70_0/libs/python/doc/html/tutorial/tutorial/exposing.html#tutorial.exposing.class_data_members)

property in python is like a static variable, which has built-in `get()` and `set()` methods. for private variables in C++ class, if there are `getter()` and `setter()` to access and set this private variables, then we can add it as a property in the wrapped python module. 




## C++ raw functions to boost.python

this is a common case especially in C projects, where is no class, but many raw functions. which can be solved by [make_funcs](https://www.boost.org/doc/libs/1_73_0/libs/python/doc/html/reference/function_invocation_and_creation/boost_python_make_function_hpp.html)


#### a.hpp

```c++
#include <iostream>

		int printA() ; 
		void setA(int nn);
		void ptest();
		void pptest();  // a public wrapper to call private member functions
		extern const int number_ ; 
		extern void aeb(void);

	typedef struct {
			float x ;
			float y ;
			struct {
					int id:100 ;
			}ForID;
	} State 

		
```


#### a.cpp


```c++
#include "a.hpp"
		const int number_ = 100 ; 
		int printA(){ return 10 ; }
		void ptest(){std::cout << "number_ is " << number_ << std::endl ; }
		void pptest(){ ptest();}
		void aeb(void){
			int a = 1 ;
			float b = 2.5;
		}
```


#### wrapper_a.cpp

```c++
#include <Python.h>
#include <boost/python/module.hpp>
#include <boost/python/make_function.hpp>
#include <boost/python/scope.hpp>
#include <boost/python.hpp> 
#include "a.hpp"

using namespace boost::python;

object printA_py(){
	return boost::python::make_function(printA);
}

BOOST_PYTHON_MODULE(aa) {	
	scope outer 
		= class_<State>("State")
			.def_readwrite("x", &State::x)
			.def_readwrite("y", &State::y)
			;
		class_<State::ForID>("ForID")
			.def_readonly("id", &State::ForID::id)
	; 

//	scope().attr("number_")= 11; 
	def("printA", boost::python::make_function(printA)) ;
	def("ptest", boost::python::make_function(ptest));
	def("aeb", boost::python::make_function(aeb));
}

```

#### build


```sh
g++ -I/home/anaconda3/envs/aeb/include/python3.6m -I/usr/local/include/boost -fPIC -fpermissive wrapper_a.cpp a.cpp  -L/usr/local/lib/ -lboost_python36 -shared -o aa.so
```




## in the end 

the performance of Boost.python is not test yet, and the big problem so far as I am handling, is the large C++ project has hundreds of internal structures, and handreds of internal functions, which creates too many handy works. not test yet if it works to only wrap the interested functions only, but ignore the remainings, mostly it won't work correctly.

so I am thinking about a simple call *.so way with `ctypes`,  there are lots of discussions about [C/C++ bind to python](https://stackoverflow.com/questions/1942298/wrapping-a-c-library-in-python-c-cython-or-ctypes), also about  [ctype performance benchmark](http://tungwaiyip.info/blog/2009/07/16/ctype_performance_benchmark), which show the ctypes is 2~3 slower than native C.




### refere


[boost.python howTo](https://wiki.python.org/moin/boost.python/HowTo)

[boost.python tutorial](https://www.boost.org/doc/libs/1_70_0/libs/python/doc/html/tutorial/index.html)

[reference manual](https://www.boost.org/doc/libs/1_73_0/libs/python/doc/html/reference/index.html)

[make_getter & make_setter sample](https://www.boost.org/doc/libs/1_58_0/libs/python/doc/v2/data_members.html#make_getter-spec)

[add_property with make_getter sample](https://www.boost.org/doc/libs/1_58_0/libs/python/doc/v2/class.html)

[c++ 11 std::function and std::bind](https://www.jianshu.com/p/f191e88dcc80)

[wrap c++ class private member](https://stackoverflow.com/questions/18391172/boost-python-wrap-c-class-private-member)

[private constructor with Boost.Python](https://stackoverflow.com/questions/43733666/private-constructor-with-boost-python)

[what are the different options ofr interfacing C with python](https://stackoverflow.com/questions/6587407/what-are-the-different-options-for-interfacing-c-or-c-with-python)






