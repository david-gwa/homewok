

## unittest 

[official refer](https://docs.python.org/3/library/unittest.html)

[in lg-sim project](https://github.com/lgsvl/PythonAPI/tree/master/tests)

### creating a unittest 

* create testcase class by subclassing unittest TestCase 
* define test as a method inside the class, name must start with `test` 
* in each test method, must call assert functions 
* call unittest.main()

the testcase output can be `OK`, `FAIL`, `ERROR`.


### assertion functions

* basic boolean asserts:

	assertEqual(arg1, arg2, msg=None)
	assertIsNot(arg1, arg2, msg=None)
	e.t.c.
	
* comparative asserts:
	
	assertAlmostEqual(first, second, places=7, msg=None, delta=None)
	// test the first and second are approximately equal by ocmputing the difference, rounding to the given number of decima places(default 7)
	e.t.c
	
* asserts for collections:

	assertListEqual(list1, list2, msg=None)
	assertTupleEqual(tuple1, tuple2, msg=None)
	assertSetEqual(set1, set2, msg=None)
	assertDictEqual(dic1, dic2, msg=None)	
	

### command line interface	

* run all unittests

	python3 -m unittest discover -v -c

* run single test module

	python3 -m unittest -v -c tests/test_XXXX.py

* run individual test case

	python3 -m unittest -v tests.test_XXX.TestCaseXXX.test_XXX
	python3 -m unittest -v tests.test_Simulator.TestSimulator.test_unload_scene


## coverage.py

[official doc](https://coverage.readthedocs.io/en/stable/)  

* (one time only) install coverage.py

	pip3 install --user coverage

* run all tests with coverage

	~/.local/bin/coverage run -m unittest discover

* generate html report

	~/.local/bin/coverage html --omit "~/.local/*","tests/*"

ps, output is in htmlcov/index.html


## logging

`logging()` supports more detail message type(info, warn, error, debug) than `print()`, and the message format is more strict with `\%`. while `print()` works both formatted message and message as string simply:

```python 
print("1+1 = ", num)
print("1+1 = %d", % num)

```


the following is a general log class, which can plug in any existing Python project:


```python

import logging 
import os 

class log(object):
    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.log.addHandler(console_handler)
    
    def set_output_file(self, filename):
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

def main():
    test = log('scenario-mm')
    file_name = "record.log" 
    dir_name = "/home/python_test/"
    try:
        os.makedirs(dir_name)
    except OSError:
        pass 
    file_path =  os.path.join(dir_name, file_name)
    test.set_output_file(file_path)
    test.log.debug("debug in episode 1...")
    test.log.info("info ...")
    test.log.warning("warn ...")
    test2 = log("zjjj")
    test2.set_output_file('record.log')
    test2.log.info("test2 info")
    test2.log.warning("test2 warn")


if __name__ == "__main__":
    main()

``` 


## pygame







