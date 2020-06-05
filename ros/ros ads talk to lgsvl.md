
## background

-------- learning is about repeat or 1000 hrs  !


this maybe the third time to go through ROS, which still looks fresh, but does give a whole picture about how ROS works in ADS dev. 

* what is ros topic and message 

the topic is the channel where nodes are subscribed for to read messages or where the nodes publish those messages; the message is the data itself, previously defined. 

```
rostopic echo [topic]

rostopic list 

rosmsg show [message]

rosrun [package_name] [node_name]

rospack find [package_name]

rosnode info [node_name]


```

* what is a publisher/subscriber

a publisher (node) publishes messages to a particular topic. [publish()](http://wiki.ros.org/roscpp/Overview/Publishers%20and%20Subscribers) is asynchronous, and only does work if there are subscribers connected on that topic. `publish()` itself is very fast, and it does as little work as possible:

```
   serialize the message to a buffer 
   push the buffer onto a queue for later processing 

```

```script
ros::Publisher advertise(const std::string& topic, uint32_t queue_size, bool latch = false);
```

the `queue size` is defined in  publihser/outgoing message queue. if publishing faster than roscpp can send the message over the wire, roscpp will start dropping OLD messages. 


```script 
ros::Subscriber subscribe(const std::string& topic, uint32_t queue_size, <callback, which may involve multiple arguments>, const ros::TransportHints& transport_hints = ros::TransportHints());
```

the queue_size is the incoming message/subscriber queue size, roscpp will use for your callback. if messages are arriving too fast and you are unable to keep up, roscpp will start throwing away OLD messages.


[in summary](https://answers.ros.org/question/243855/how-do-publishersubscriber-message-queues-work/): 


    * publish() is asynchronous.
    * When you publish, messages are pushed into a queue (A) for later processing. This queue is immediately pushed into the outgoing/publisher queue (B) . PS: If no one subscribes to the topic, the end is here.
    * When a subscriber subscribes to that topic. Messages will be sent/pushed from the corresponding outgoing/publisher queue (B) to the incoming/subscriber queue (C).--> this is done by internal thread
    * When you spin/ callback, the messages handled are from the incoming/subscriber queue (C).


* [messages](http://wiki.ros.org/Messages)

**msg** files are simple text files for specifying the data structure of a message. These files are stored in the msg subdirectory of a package. the publisher and subscriber must send and receive the same **type/topic** of message


```
{"op": "publish", "topic": "/talker", "msg": {"data" : "_my_message" }}
```


## ads ros pipeline 


[understand rosbridge:  simple ROS UI](https://msadowski.github.io/ros-web-tutorial-pt1/)

[roslibjs](http://wiki.ros.org/roslibjs/Tutorials/BasicRosFunctionality)



## rosBridge in lgsvl 

rosbridge is an adapter for non-ros apps to talk with ros. it's common to package ADS software as ros node during dev stage, and rosbridge is the common way to integrate simulator with ADS software.

the base implementation of `rosBridge` in lgsvl is as following: 


#### RosBridge.cs 

```
ConcurrentQueue<Action>  QueuedActions ;
Dictionary<string, Tuple<Func<JSONNode, object>, List<Action<object>>>> Readers ;
```

the topic is packaged as:

```
{ "op":  "subscribe or publish or call_service or service_response or set_level",
  "topic":  {},
  "type":  {}
}

```

* AddReader(topic, callback)

a few types supported:  Deteced3DObjectArray, Deteced2DObjectArray, VehicleControlData, Autoware.VehicleCmd, TwistStamped, Apollo.control_command 

which is the list of ros messagees that lgsvl can parsing.


```
if(!Readers.ContainsKey(topic))
{
   Readers.Add(topic, Tuple.Create<Func<JSONNode, object>, List<Action<object>>>(msg=>converter(msg),  new List<Action<object>>()) ) ;

}  

Readers[topic].Item2.Add(msg=>callback(T)msg)); 

``` 

`AddReader` is the subscriber nodes in lgsvl. in `Sensor` group, there are three sensors do `AddReader`: 

         GroundTruth3DVisualizer 
  
         VehicleControlSensor 

         GroudTruth2DVisualizer


which means, lgsvl server can read these three typies of messsages. 

if there is no rendering/visual needs, only vehicle conroller (acc, brake) message is required for lgsvl. 


* AddWriter(topic)

the types/topic supported are:  ImageData, PointCloudData, Detected3DObjectData, Detected2DObjectData, SignalDataArray, DetectedRadarObjectData, CanBusData, GpsData, ImuData, CorrectedImuData, GpsOdometryData, ClockData.


`AddWriter()` is a writer adapter, which returns a special type/topic writer/publisher. `AddWriter` is the publisher nodes in lgsvl, in `Sensor` group, the following sensors can publish message out:

		LidarSensor 
		SignalSensor
 		GpsInsSensor
		GpsOdometrySensor
		DepthCameraSensor
		ImuSensor
		SemanticCameraSensor
		GroudTruth2DSensor
		CanBusSensor
		RadarSensor
		GroudTruth3DSensor
		ClockSensor
		GpsSensor
		ColorCameraSensor


* AddService(topic, callback)


* OnMessage(sender, args)

```
if (args.op=="publish")
{
   topic = json["topic"]
   Readers.TryGetValue(topic, out readerPair)
   var parse = readerPair.Item1 ; 
   var readers = readerPair.Item2; 
   var msg = parse(json["msg"]);
   foreach (var reader in readers)
   {
     QueuedActions.Enqueue(()=>reader(msg));   //
   }
```

ros subscriber uses a callback mechanism, when the message is coming, all readers who subscribe this topic will read in this message. 


#### RosWriter.cs 

the message output is in the format as:

```
 { 
   "op" :  "publish" ,
   "topic" :  Topic, 
   "msg":  message 
 } 

```
 
#### websocket in ros bridge 

the implementation of ros bridge in lgsvl is by `WebSocket`, which maintained a continously communication pipeline, for external ros nodes publishers.


## ros ads talk to lgsvl rosbridge 

from the previous section, lgsvl talk to external ros nodes (which is the ADS stack) through rosbridge, and which needs external inputs, e.g. vehicle control command, 2d/3d ground truth visualizer. and the ADS stack ros nodes can subscribes Gps, canbus, Lidar, Radar, GroudTruth, SemanticCamera, DeepCamera topics through lgsvl rosbrige.

so the pipeline are simple as following:

```
	lgsvl rosbridge  -->  {gps, radar, camera, lidar, groudTruth message} -->  ADS stack nodes 

	ADS stack nodes -->  {vehicle control command message} --> lgsvl rosbridge 

```
 

usually, the ADS stack nodes are a few related ros nodes, including RTK/GPS sensor, Lidar/Camera sensor, hdmap node, data fusion node e.t.c.


#### run ROS ADS stack

the following nodes are used commonly in ADS dev:

* sensor_node

subscribe: `/gps`, `/odom` e.t.c topics

publish: `/sensor/data` topics

* hdmap_node

subcribe: `/rtk/data`, `/ins/data` topics. 

publish:  `/lane/info`,  `/speed_limit` e.t.c. topics

* fusion_node 

subscribe topics: `/canbus`, `rtk/data`, `/ifv_lane`,  `/radar/blind`, `/radar/corner`, `/esr`, `/velodey`,  `/lane/info` e.t.c

publish topics: `/object_list/`, `/road/info`, `/vehicle/status` and visual related messages e.t.c.

* planning_node 

subscribe topics:  `/object_list`,  `/road/info`, `/vehicle/status` from fusion_node

publish topics: `/vehicle/cmd_ctl` 


#### system verification

ros is a common solution to package ADS stack and integrate with the simulation env during SIL sysem verification. there maybe some changes when setup the ADS stack in physical vehicle, due to the hardware computing limitation, drivers e.t.c, which gives another topic about how to quick build up a user-friend verification pipeline for both simulation verification and physical verification. 


## refer

[ros overview](http://wiki.ros.org/ROS/Tutorials)



























