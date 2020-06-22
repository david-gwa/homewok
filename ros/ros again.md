
## ros eco

deep into ros eco-system for a while


#### ros msgs

* message_generation

* message_runtime ?


* std_msgs/ByteMultiArray

* sensor_msgs/NavSatFix 

* geometry_msgs/






###### how to create a new msgs 

[Writing a ROS Python Makefile](http://wiki.ros.org/rospy_tutorials/Tutorials/Makefile)

[create a ros msg](http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv#Common_step_for_msg_and_srv)

for the `package.yml` should at least include the following lines:

```yml
  <buildtool_depend>catkin</buildtool_depend>
  <build_depend>message_generation</build_depend>
  <build_export_depend>rospy</build_export_depend>
  <build_export_depend>std_msgs</build_export_depend>
  <exec_depend>rospy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
```


for the msg `CMakeList.txt`:

```yml
find_package(catkin REQUIED COMPONENTS
	roscpp
	rospy
	std_msgs
	message_generation
) 

add_message_files(
	FILES
	custom.msg
)

generate_messages(
	DEPENDENCIES
	std_msgs
)
```

then `catkin_make` will create `custom message` at `/devel/includes`	

```sh
rosmsg show my_pkg/custom_msg
```

go to `~/catkin_ws/devel/lib/python2.7/dist-packages/my_msg_py/msg`, check the generated custom message python module, which can add to `$PYTHONPATH` for later usage








#### ros node

###### how to create a new ros node 

[creating pack & nodes](https://industrial-training-master.readthedocs.io/en/melodic/_source/session1/Creating-a-ROS-Package-and-Node.html)


* create a package(my_pkg) inside `~/catkin_ws`

* write the package code 


* CMakeLists.txt 

```yml
add_compile_options(-std=c++11)
add_executable(vision_node src/vision_node.cpp)
target_link_libraries(vision_node ${catkin_LIBRARIES})
```

* a simple node

```c++
#include <ros/ros.h>
int main(int argc, char* argv[]){
	ros::init(argc, argv, "demo_node");
	ros::NodeHandle nh ;
	ros::spin();
}
```

* run the test 

```sh
roscore &
source ~/catkin_ws/devel/setup.bash
rosrun my_pkg demo_node
```

###### how to create a new ros node with catkin 

preparation, check your `$ROS_PAKCAGE_PATH`, the default pkg path is `/opt/ros/kinetic/share`, append custom pkgs path from `~/cakin_ws/devel/share`. 

```sh
cd ~/my_catkin_ws/src
catkin_create_pkg my_pkg [dependencies, e.g. sd_msgs rospy]
rospack find
```

###### sensor serial data to ros node

sensors(e.g. rtk, imu) to ros is communication from external world to ros sys. Things need to take care:  mostly sensor hardware device doesn't support ROS driver directly, so first need device serial or CAN to get the raw sensor data, and package it as `sensor/raw_msg` to publish out; the real ros-defined sensor node, will subscribe `sensor/raw_msg` and publish the repackaged `sensor/data` to the ros system, (which usually happened in ros callback).

```py
def rtk_cb(std_msgs::ByteMultiArray raw_msg):
    rtk_msg = func(raw_msg)
    pub.publish(rtk_msg)

pub = nodeHandler.advertise<sensor_msgs:NavSatFix>("/rtk_gps/data", 1)
sub = nodeHandler.subscribe("/rtk_gps/raw_data", 1, rtk_cb)

def raw_data_generator():
	try:	
		with open("/dev/ttyS0", "r|w") as fd:
			header = read(fd, buf, header_line)
			while ros::ok():
				content = read(fd, buf, content_lines)
				std::msgs::ByteMultiArray raw_msg 
				raw_msg.data.push_back(header)
				raw_msg.data.push_back(content)	
				pub.publish(raw_msg)
		close(fd)
	except:
		print("failed to read raw data\n")

```

#### sensor data goto CanCard

sensors(such as camera, radar, lidar e.t.c) go to ros sys through Veh CAN Bus. the difference between **CAN** msg and **serial** msg is data atomicity. as serial msg is only one variable, which gurantee atomicity in application level;  while each CAN frame usually include a few variables, which need custom implement atomicity in application level. 

```py 

thread0 = pthread_create(recv_thread, raw_can_data)
thread1 = pthread_create(send_thread)

def thread0():
 	 recv_data = func(raw_can_data)
	 pthread_mutex_lock(mutex_lock)
	 sensor_raw = recv_data 
	 sem_post(sem_0)
	 pthread_mutex_unlock(mutex_lock)

def thread1():
	pthread_mutex_lock(mutex_lock)
	sensor_ros_msg =  sensor_raw 
	pthread_mutex_unlock(mutex_lock)
	node_.publish(sensor_ros_msg)

```




#### ros node to external device


another kind of communication, is from ros system to external device/env, such as dSPACE. the external device, if not communication through serial, then usually support Ethernet(udp/tcp), which then need to implement a custom udp/tcp data recv/send func. the ros node subscribe the necessary data, then send it out through udp/tcp.


```py 
def cb(sensor_msg):
	data = repack(sensor_msg)
	udp.send(data)

sub = nodeHandler.subscribe("/useful/data", 1, cb)
```









#### TCPROS

ROS通过远程过程调用交换XML-PRC信息来实现与Master节点的通信，在节点之间的话题和服务数据流被编码成自定义的TCPROS协议，ROS的连接地址符合URI格式

[tcpros understanding 1](https://zhuanlan.zhihu.com/p/36055291)

每一个ROS节点具备一个XML-RPC服务(parameter server)

how ros master keep heartbeat with ros nodes (**连接模型**)：

一个节点注册它的发布或订阅的话题到master节点，每一个话题publisher通过registerPublisher()的远程过程调用注册到Master节点，每一个话题的subscriber通过registerSubscriber()的远程过程调用注册到Master。Master通过同一个话题连接发布者和订阅者。

in code, `nodeHandler.advertise()` called in publisher/subscriber node, to register their topices to ros master.



当一个节点向master注册它的订阅话题成功时，master会返回一个包含发布者URIs信息的应答。因此subscriber和publisher就可以建立连接，之后就可以传输数据。当一个新的publishser注册到master后，master会启动publisherUpdate()通知所有的subscriber更新可用的publisher的URI列表，之后数据流就可以通过TCPROS进行交换。



XML-RPC提供了一个简单清晰的协议用于远程过程调用。实际数据流传输协议是tcpros, 

**消息结构**, ROS中的消息以32位小端模式存储，它适用于大部分的x86以及ARM体系。


#### ros build(catkin) 


#### ros visual(rviz)

[ros-rviz](https://github.com/jstnhuang/ros-rviz)

* how rviz works ?

If you want to create a node providing a set of interactive markers, you need to instantiate an InteractiveMarkerServer object. This will handle the connection to the client (usually RViz) and make sure that all changes you make are being transmitted and that your application is being notified of all the actions the user performs on the interactive markers. 

![image](http://wiki.ros.org/rviz/Tutorials/Interactive%20Markers:%20Getting%20Started?action=AttachFile&do=get&target=interactive_marker_architecture.png)


UDP-based for latency-sensitive applications

* package, logically constitues an useful module, e.g. ROS nodes, libs, data sets; 

* stack, a container of packages which share a common goal. e.g. computer vision, or motion planning


* [ros探索总结: rviz](https://www.guyuehome.com/2213)

```sh
rosrun rviz rviz
```

进行数据可视化的前提当然是要有数据，假设需要可视化的数据以对应的消息类型发布，我们在rviz中使用相应的插件订阅该消息即可实现显示。

* MarkerArray

* BlindRL

* CornerFL





#### rviz 可视化 rosbag

**rviz config** can customize the rviz display


原理： 收到pkg_msg, 将sensor_pkg消息打包成对应marker/markerArray 结构体，再将其publish。
实现： 定义接收pkg_msg的节点，其subscribe()回调执行对应markerArray结构体publish()

```python 
ros::Publisher markerArray 
def pkg_cb(sensor_pkg):
	for objIdx in sensor_pkg.ObjNum:
		prepare_marker(marker, sensor_pkg.objects[objIdx]
		SensorDisplay.markers.append(marker)	
	markerArray.publish(SensorDisplay)
	SensorDisplay->markers.clear()

subPkg = nodeHandler.subscribe("sensor_pkg", 1, pkg_cb);
markerArray = nodeHandler.advertise<visulization_msgs::MarkerArray>("sensor_pkg", 1)

```






#### rosbag(record, play)



## ros tools

```sh
rosbag play test.bag
rosbag info test.bag
rosbag record -a  
rosbag record -0 subset msg1 msg2
rosrun rviz rviz
rostopic list -v 
rospack find std_msgs  #
catkin_make --pkg your_custom_pkg

```


[ros_qtc_plugin](https://github.com/ros-industrial/ros_qtc_plugin)

[ros camera data collection and transfer](https://blog.csdn.net/LOVE1055259415/article/details/80216570)




#### data collection

* ros node/driver in device ? 

#### data analysis

* rosbag split

check github for more rosbag tools


## mf4 eco

* Vector mf4Lib && asammdf 

####  mf4 parser 



#### mf4/rosbag adapter 


## data driven pipeline

data in either rosbag or mf4, the examples of module under test(MUT) are: fusion, planning, AEB e.t.c.

### modules debugging 

when there are bugs in the existing module. we can feed the module with data, and check/log all the necessary internal variables to check where the bugs are.

tools support: data driven debugging pipeline for each module. most importantly is during module development need welled-define internal variables in each module, which are the keys to help find out the problems of the modules/subsystem.

and to speak out the key internal variables, should be very familar with the subsystem, or have high experience in the special modules. e.g. an expert who is very know-how of the fusion system, can define the internal KPIs.


### modules performance 

when need to test the modules performance or function boundaries. which requies massively test to cover the known scenarios and as most unknown scenarios as possible. 

tools support: either a bash job pipeline, or a well-defined micro-services framework to help massively test, both require DevOps team to support, from hardware to software; as well as a robost automatic workflow, which includes data preparation automaticly; module test automatically, which should include automaticlly evaluation metrixes, and automatically post analysis, e.g. KPI visualization


some example of evaluation metrixes: 

* aeb, false positive/false negative evaluation 

* fusion, the goal of the ev


## after-market data pipeline

depends on more components: vehicle-side, cloud-side. 

#### vehicle side 

* chips, computing power/network interface/Tbox/customer services 

* funcs: log trigger system, data uploading system

#### cloud side 

goal: to optimize/expand func performance/boundaries of the ADS system


tech does acc busniess behavior, e.g. creating more consuming products, or improve human lives, e.g. more healthy and happier.



## comments

* features accumulation dev  vs agile feature accumulation

* deep into ros eco-system

* configure management, docker harbor, gitlab, jekins 

* frameworks, a set of tools and libs. 




## refere








