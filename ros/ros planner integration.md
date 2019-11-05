
/home/wubantu/zj/lg-ros/catkin_ws/src/rtk_sensor/src/main.cpp:4:32: fatal error: nmea_msgs/Sentence.h: No such file or directory


## install a missing ROS messge 

[sol](https://answers.ros.org/question/9201/how-do-i-install-a-missing-ros-package/)

rosdep  update 

rosdep  install nmea_msgs

sudo apt-get install ros-lunar-nmea-msgs 

[sol1](https://answers.ros.org/question/9197/for-new-package-downloading/)



## catkin_make 

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


## rosrun failed 

[rosrun] Couldn't find executable named rtk_sensor below /home/wubantu/zj/lg-ros/catkin_ws/src/rtk_sensor
[rosrun] Found the following, but they're either not files,
[rosrun] or not executable:



in  rtk_sensor.CMAKEList.txt  add:

catkin_package(
#  INCLUDE_DIRS include
  LIBRARIES rtk_sensor
  CATKIN_DEPENDS roscpp std_msgs
  DEPENDS system_lib
)




