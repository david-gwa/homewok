
### background

ros is helpful to connect differrent sensor nodes, analysis nodes together, which is used a lot in self-driving.


### ros filesystem tools

first, check `ROS_PACKAGE_PATH`, where defines all ROS packages that are within the directories. 

```shell

rospack find [package-name]

rospack list 

roscd [package-name]

```

take an example, how to locate `rosbridge_websocket.launch`:

```shell

rospack find rosbridge*    #rosbridge_server
roscd rosbridge_server
cd launch 

```

another tool to view ros-launch: `roslaunch-logs`



## launch file

launch files, which uses XML format, usually make a directory named "launch" inside the workspace to organize all launch files, and it provides a convenient way to start up multiple nodes and master.

process in a [depth-first tarversal order](http://wiki.ros.org/roslaunch/XML), 

```shell

roslaunch package_name launch_file
#or 
roslaunch /path/to/launch_file
```


an sample launch file:

```xml
<launch> 
 
   <node pkg="package_name"  type=" "   name=" "  output=" " args=" " />
   
</launch>
```

`args` can define either env variables or a command. 

`[node/type](http://wiki.ros.org/roslaunch/XML/node)` There must be a corresponding executable with the same name. 



### rviz 

test run:

```shell
# terminal 1 
roscore 

# terminal 2 
rosrun rviz rviz 

``` 

### rosbag

[common commands](http://wiki.ros.org/rosbag/Commandline):

```shell
rosbag record #use to write a bag file wit contents on the specified topics
rosbag info #display the contents of bag files 
rosbag play #play back bag file in a time-synchronized fashion
```

there are [APIs](http://wiki.ros.org/rosbag/Code%20API) to read/write ros bags. 



### kitti rosbag 

[official raw data](http://www.cvlibs.net/datasets/kitti/raw_data.php)


### message_filter
[ros filter](http://wiki.ros.org/message_filters)


According to the loaded plugin descriptions the class jsk_rviz_plugin/BoundingBoxArray with base class type rviz::Display does not exist. 


### add launch to CmakeList build

if self defined `node/type`, it can be put in `/package_name/scripts/type.py`



### ros package 

```shell

mkdir -p ~/catkin_ws/src
cd ~/catkind_ws/src
catkin_create_pgk demo std_msgs rviz 
cd demo
mkdir launch
cat "<launch> <node  name="demo"  type="rviz" -d="ls `pwd`" /> </launch> " >  demo.launch
cd ~/catkin_ws
catkin_make --pkg demo

# add catkin_ws to 
cat "export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/path/to/catkin_ws/" >> ~/.bashrc


```








