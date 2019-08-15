
##  Scenario runner 

* load scenario configuration 

* load scenario & manager

* trigger scenario execution


### functions 
* to run(and repeat) a single scenario or a list of scenarios 

* define a list of scenarios 

### api design

class run_scenarios()
{ 

 __init()

prepare_ego_vehicle()

analyze_scenario(){sucess or failure}

load_world()

load_run_scenario(){load simManager & run simManager) 

run(){setup repetitions ;  if openScen run_openScenario() }

cleanup() 

run_openScenario() {config = OpenScenarioConfiguration(openScenpath); }

}


class OpenScenaroConfguration(config)
{

   __init__ 

   __parse_openScenario_config();

   
   class OpenScenarioParser()
//     Pure static class providing conversions from OpenScenario elements to ScenarioRunner elements

}


class Scenario()
{
  //a base class to hold behavior_tree describing the scenario & test criteria 

  __init__(){ behavior,  test_criteria=py_trees, } 

}

class ScenarioManager()
{
  //a base class to hold all functionality required to start, analysze a scenario 
  
  __init__()

  load_scenario()

  run_scenario()

  analyze_scenario()

} 
  



  
## design document for scenario APIs

###  scenario manager class  

// public interface: 
   load_scenario(scenario);
   run_scenario();
   analyze_scenario(stdout, filename);  //scenario report
   stop_scenario(); 
  
// member variables :
    scenario_class (category, allow multi tags)
    ego_vehicle
    other_actors
    scenario 
    scenario_tree(?)
    

### Scenario structure

// member variables:
     test_criteria; 
     criteria_tree(add test_criteria)
     behavior(?) ;
     scenario_tree (?) (add behavior, criteria_tree)
     timeout;
     
### scenario runner 

support command line configure_file,  command line single scenario

// public interfaces:
    prepare_ego_vehicles(config);
    analyze_scenario(args, config) =>  manager.anlyze_scenario();
    load_world(args, map)
    load_and_run_scenario(args, config, scenario)
    run(args){get specific user-defined scenario type, initialize it, load and run it}
    run_openscenario();
// to support job list run
    run_by_category(category_type: odd, oedr, maneuver)

    
// member variables:
     world,
     manager, 
     timeout,


### base scenario

// virtual inerfaces:
    _initialize_actors(config);
    _setup_scenario_trigger(config);
    _create_behavior();
    _create_test_criteria();
    _trigger_behavior();

    
// variables:
     ego, 
     npcs,
     timeout,
     category,
     criteria_list,
     map
     name,
     teriminate_on_failure
     scenario_uid , 
     maneuver == null ,
     odd == main_lane ,
     oedr == static_obj 

      
### user defined scenario 
derived from BaseSceenes(odd==main_lane, oedr==static_obj, maneuver, scenario_uid = check_table[id]), implement the virtual interfaces specially 

//maitain a public check_table dictionary <uid, odd-oedr-maneuvor>



### scenes with varieties (parameters to iterate) 
### general API interface
  


## scenario builder 


### scenario run criteria 

* run_timeout 
* collision_trigger
* test_criteria & test metrics 


### ODD dictionary <type, list<> >

### how to design actor time-event

 npc  sudden-stop

 ego acc/dec

 ego lane-change


### test_criteria in scenario_runner

e.g. max velocity,  driven distance,  collision, kl, reachedRegion, onSidewalk,  WrongLane... 

test_criteria will be called during analyze_scenario()



### timeout


### behavior 
行为定义： npc走到下一个路口， 子行为：follow wp, 进入下一个路口区域 ;
定义停止条件： 到达下一个路口区域，停车

场景行为定义： e.g. 跟车

npc先停3秒，等EGO进入预订出发区域；
npc朝障碍物运动，暂停，等障碍物清理，朝下一个路口，进入下一个路口，npc停车
结果判定: 1) npc, ego停在预定区域，且相距20M以内  2）ego状态为停



e.g. distance trigger,  velocity trigger,  in tim trigger, keep velocity, stop vehicle 


/b(all criteria, timeout, behavior compose the scenario_event_trigger, which will lead to terminate the scenario)

scenario_tree.add_child(scenario.behavior) --> 
scenario_tree = py_trees.composites.Parallel()

scenarioManager.run_scenario()
{
  based on  scenario_tree.status ? 
  while _running:
     sleep()
}

scenarioManager._tick_scenario()
{
  scenario_tree.tick_once() 
  if(scenario_tree.status 1= running):  _running=False
}
   
   

## py_trees

Q: figure out how atomic_behavior.update() works in scenario runner? 

behavior is defined inside each scenario, which futhure only called in ScenarioManager  





py_trees.common.Status 

py_trees.common.ParallelPolicy.SUCCESS_ON_ONE



## scenario_tree.tick_once() error

type object 'SuccessOnOne' has no attribute 'synchronise'


check py_trees version

in [Carla.ScenarioRunner](https://github.com/carla-simulator/scenario_runner/blob/master/Docs/getting_started.md), it mentioned,  py-trees==0.8.3 


current installed py_trees.__version__ = 1.12


change back to 0.8.3 ?

pip show py_trees 
pip uninstall py_trees 
pip install py_trees==0.8.3 



FOllow closest lane speed 6.24, 0.43
CollisionTest.update()[Status.RUNNING->Status.RUNNING]
CollisionTest.update()[Status.RUNNING->Status.RUNNING]
Status.RUNNING
debug: tick_scenario
test in run_scenario ...
on_server_tick get velocity 0.00
on_server_tick get velocity 0.00
FOllow closest lane speed 0.00, 0.00



followClosest_lane() call once for all, if update() everytime, doesn't work.



the problem is  sim.run() and self._tick_scenario(){npc.followclosestlane()} is in two different thread?




### lg scenario callback mechanism 


callback invoked inside Simulator.run() and while a callback is running, the simulation time is paused.





### set velocity in run-time

```shell 
while True:
	sim.run(0.5)
	npc.set_velocity(speed)
``` 
 

carla has `episode` concept, so it's easy  to get the agents state from each `episode`.

 

```c++

auto GetActorDynamicState(actor):
	_episode->GetState()->GetActorState(actor.id);

auto GetActorLocation(actor):
	return GetActorDynamicState(actor).transform.location;

geom::Location GetLocation():
	return  GetEpisode().Lock()->GetActorLocation(*this)

.def ("get_location",  &cc::Actor::GetLocation)

```

# why websocket

## background 

http only allow client request server

websocket allow both ways, client request server, and server sent update notification to client without client request


## lg simulator 

```python
commond: 
    asyncio.run_coroutine_threadsafe(self.websocket.send(data), self.loop)

```

only client to server ?  how to add server update notification to client ? 


## rpc vs  websocket

we need lg simulator server to return state of each episode 

TODO: study on rpclib

TODO:  [HTTP vs  TCP stream vs websockets](https://github.com/Storj/core/issues/490)

rpc is good at  data syncronization, client directly call server functions

websocket is good at data stream, 


### real-time application with websocket 

goal:  serve gets the ability to push to clients without client requesting data first 

a not efficient way: client request data from server every fixedTime.

a better way: server sends data to client when state update


### unity fixed update 

[fixed update is fixed episode?](https://www.cnblogs.com/murongxiaopifu/p/7683140.html)

[is Unity mutli-thread](https://forum.unity.com/threads/is-unity-multi-threaded.67879/)

[web aplication messaging protocol](https://wamp-proto.org/)


### python websocket server 



### unity clientRpc 

[retired function]


### websocket.onMessage()

This event acts as a client's ear to the server. Whenever the server sends data, the onmessage event gets fired.

struct ClientAction
{
  public ICommand  Command ;
  public ICommand  Arguments;
}



###  threading.Thread

### JSONObject

### websocketBehavior


## test case: unity Editor connect with python

ConnectionRefusedError: [Errno 111] Connect call failed ('127.0.0.1', 8181)

```shell
netstat -tulnp | grep <port no>
sudo netstat -lp
```

## message push

define a episode class in ApiManager, and the websocket.server will send an episode to client 

[refer1](https://blog.csdn.net/w1992wishes/article/details/79583543)

[refer2](https://www.cnblogs.com/GoCircle/p/7871982.html)

[refer3](https://www.sitepoint.com/real-time-apps-websockets-server-sent-events/)

[refer4](https://yq.aliyun.com/articles/323585)

[refer5](https://www.cnblogs.com/stoneniqiu/p/8488150.html)

* client 

```c# 

client.onmssage = function(msg){
	alert(msg.data);
};

```

* server 

```c#
@OnMessage
OnMesssage(String message)
{
}
``` 


## Fleck 

[git](https://github.com/statianzo/Fleck)



## websocket-sharp

[refer1](https://www.cnblogs.com/xiaoqi/p/websocket-sharp.html)


* server side 
```c#

 class Lua : WebSocketBehavior{ 
   void OnMessage(MessageEventArgs e)
   {
      var msg =  e.Data = "string " ;
      Send(msg);
   }
 }

 class ApiManager {
	Server = new WebSocketServer(Port);
	Server.AddWebSocketService<Lua>;
	Server.Star();
	
```


 






















