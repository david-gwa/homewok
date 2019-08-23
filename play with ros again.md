
a few month later, when back to a ros project, almost lost, where should start ?


## how ros master works ?

[ros recap and core concepts](https://zhuanlan.zhihu.com/p/67442943)

ros master is triggered when running `roscore`, namely ros nodes manager

for each ros node start, it will register at ros master, to tell about itself(node) and its broadcast/receive topic

when the sender node is already in ROS, rosore will send "sender node" existing info to the receiver node, and the receiver node will request a TCP/UDP talk to the sender node. and `roscore` task is done 



## ros package manage

* create ros workspace 

* create ros package under workspace 

* build ros package

### build ros module 

#### ros module header 

to create a new user-specified ros module, will refer/link some standard message modules, e.g. geometry_msgs, pcl_msgs e.t.c

the standard message modules are located at `$ROS_PACKAGE_PATH`

for any external message modules that not located at `$ROS_PACKAGE_PATH`, need add to this path, so build system can find it correctly.

#### .msg file

it's the messsage protocol, which will be compiled as `.h` file, and then used to compile ros node binary


## ros modules run

```shell

cd /ros/project 
source ./devel/setup.bash
rospack list 

```

to start a ROS project, there needs to start `roscore` at first, then all other ros nodes, (no order need). usually it's efficient to manage all the ros thread starting in one start script. 


* roscore 

* rosrun 

* roslaunch

the difference between `rosrun` and `roslaunch` is that,  `roslaunch` does spawn a new process for the node, and then pipe the output to a log file; while `rosrun` only run the node in current terminal 


### dev tool

refer to `apollo ros intro`
### debug tool

### rosbuild vs catkin 

### message vs topic 

topic is the container of communication in two node peers, and message is the content in the container(topic)


### catkin_make 

`catkin_make` should be called from catkin workspace

for msgs_node, which will be used in other ros node, should compile first, by 
`catkin_make --pkg msgs_node`


if the ros node should be executable in later, modify the node CMakeLists.txt by:

```shell

catkin_packag(

LIBRARIES rtk_sensor
CATKIN_DEPENDS roscpp  std_msgs 
DEPENDS system_lib 
)

```



### ros bridge


### URDF


### add new message type into ros system











