# how to write python unittest 


## unittest.TestCase

any user defined test class should first derived from `unittest.TestCase` 
 
## setUp() & tearDown()

setUp() provides the way to set up things before running any method starting with `test_xx()`  in user defined test class. tearDown() is where to end the setting ups 


## test with other modules/class

usually the class/methods we try to test have depends on other modules/class, but as unit test want to isolate these depends, so either mock the other methods or fake data. in general there are three types of depends:

### pure variable 

this is the most simple case, then you can directly define the same pure type variable in your `test_xx()` method 


### methods in other modules  
here need t use `patch`, to mock the method and define its return value is your `test_xx()` method, then in the class where call the real method will be replace by this mocked one.

### methods in other class 
here need to use `mock`, either MagicMock or Mock will works.


## test with while Loop
TODO

## test with raise Error
TODO

## sample unit test 

```python 
import unittest
import math
import py_trees
import lgsvl 

from .common import spawnState, cmEqual, notAlmostEqual
from scenario.server_data_provider import *
#from scenario.server_data_provider import calculate_velocity
from mock import MagicMock, patch 

class TestServerDataProvider(unittest.TestCase):

    def setUp(self):
        pass

    def test_calculate_velocity(self):
        velocity =  lgsvl.Vector(1.0, 0.0, 0.0) 
        self.assertEqual(calculate_velocity(velocity), 1.0, "calculate velocity")

    def testjson2vector(self):
        jdic = {'x': 1.0, 'y':0.0, 'z':0.0 }
        cmEqual(self, json2vector(jdic), lgsvl.Vector(1.0, 0.0, 0.0), "json2vector with dict input")
        jdic2 = "string"
        raised = False 
        try: 
            json2vector(jdic2)
        except:
            raised = True 
        self.assertTrue(raised, 'j2v with string input')

    def test_register_actor(self):
        actor = "actor"
        provider = ServerDataProvider()
        try:
            provider.register_actor(actor) 
        except Exception as exception:
            print(exception)
        self.assertIs(provider.id2actor[0], actor)
        with self.assertRaises(KeyError):
            provider.register_actor(actor)

    def test_get_velocity(self):
        vmap = {"actor": 10.0}
        provider = ServerDataProvider()
        ServerDataProvider._actor_velocity_map = vmap
        self.assertEqual(provider.get_velocity("actor"), 10.0)
        self.assertEqual(provider.get_velocity("none"), 0.0)

    def test_get_location(self):
        vmap = {"actor": 10.0}
        provider = ServerDataProvider()
        ServerDataProvider._actor_location_map = vmap
        self.assertEqual(provider.get_location("actor"), 10.0)
        self.assertEqual(provider.get_location("none"), None)
    
    def test_cleanup(self):
        provider = ServerDataProvider()
        provider.cleanup()
        self.assertEqual(len(ServerDataProvider.id2actor), 0)
        self.assertEqual(len(ServerDataProvider._actor_velocity_map), 0)
        self.assertEqual(len(ServerDataProvider._actor_location_map), 0)

    @patch("scenario.server_data_provider.calculate_velocity")
    def test_on_server_tick(self, mock_vel):
        vec = lgsvl.Vector(1.0, 1.0, 1.0)
        mock_vel.return_value = 10.0
        episode_state = {"npcs_state": [{"velocity":{"x": 1.0, "y": 1.0, "z": 1.0},
                                        "transform":{"position":{"x": 1.0, "y": 1.0, "z": 1.0}} }] }
        ServerDataProvider.id2actor = {0: "actor0"}
        provider = ServerDataProvider()
        provider.on_server_tick(episode_state)
        self.assertIs(ServerDataProvider._actor_velocity_map["actor0"], 10.0)
        cmEqual(self, ServerDataProvider._actor_location_map["actor0"], vec, "ocation match test")


    def create_EGO(self, sim): # Only create an EGO is none are already spawned
        return sim.add_agent("XE_Rigged-apollo", lgsvl.AgentType.EGO, spawnState(sim))
    
    def create_NPC(self, sim): # Only create an EGO is none are already spawned
        return sim.add_agent("Sedan", lgsvl.AgentType.NPC, spawnState(sim, 1))
		
```


## refer

[unittest + mock + tox](https://www.jianshu.com/p/013b9bdecb0d)























