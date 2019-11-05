

## autoware.AI 

[introduction doc](https://gitlab.com/autowarefoundation/autoware.ai/autoware/wikis/home) 

* localization 

HD map, NDT algorithm ->  Kalman Filter with odometry data from CAN and GNSS/IMU sensors

* detection 

camera + Lidar with HD map ->  deep learning and sensor fusion 

* tracking 

Kalman Filter with lane networking 

* prediction 

probabilistic robotics and rule-based systems, partly deep learning 

* control

a twist of velocity and angular-velocity 


## install autoware in Ubuntu16.04

[build link](https://gitlab.com/autowarefoundation/autoware.ai/autoware/wikis/Source-Build)

```shell

sudo apt-get update 

sudo apt-get install python-catkin-pkg  python-rosdep ros-lunar-catkin gksu 
sudo apt install -y python3-pip python3-colcon-common-extensions python3-setuptools python3-vcstool
pip3 install -U setuptools
mkdir -p autoware.ai/src 
cd autoware.ai 
wget -O autoware.ai.repos "https://gitlab.com/autowarefoundation/autoware.ai/autoware/raw/1.12.0/autoware.ai.repos?inline=false"
vcs import src \< autoware.ai.repos
rosdep update    #failed
rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release  #without CUDA 

```


error message:

ERROR: the following packages/stacks could not have their rosdep keys resolved
to system dependencies:
vector_map: Cannot locate rosdep definition for [visualization_msgs]


	is there error due to $ROS_DISTRO=lunar, in official which requires for `Kinetic` 








## simulation with ROSBAG 










