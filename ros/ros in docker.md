


[docker 1.10 container's IP in LAN](https://stackoverflow.com/questions/35742807/docker-1-10-containers-ip-in-lan/39285950#39285950)

[jessfraz](https://blog.jessfraz.com/)

#### run dockerimage

```
docker build -t ads_ros . 

docker run -it ads_ros  /bin/bash

```

#### update ros packages using rosdep 


[rosdep](http://wiki.ros.org/rosdep)


#### unable to run `cakin_make` in dockerfile 

```
RUN /bin/bash -c '. /opt/ros/kinetic/setup.bash; cd <into the desired folder e.g. ~/catkin_ws/src>; catkin_make'

``` 


#### dockerfile for ads ros


``` 
FROM ros:kinetic 

# create local catkin workspace 
ENV CATKIN_WS=/root/catkin_ws
ENV ROS_DISTRO=kinetic
RUN mkdir -p $CATKIN_WS/src

## install catkin_make 
## https://docs.ros.org/api/catkin/html/user_guide/installation.html
RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        build-essential \
        apt-utils \
        ca-certificates \ 
        psmisc \
        cmake \
        vim \ 
        python-catkin-pkg \ 
        ros-${ROS_DISTRO}-catkin  \ 
        ros-${ROS_DISTRO}-tf  \
        ros-${ROS_DISTRO}-turtlesim \
        ros-${CATKIN_WS}-rosbridge-suite 
        iputils-ping \   
        net-tools 
### add rapidjson include  header
COPY /rapidjson /usr/include/rapidjson 

# RUN source ~/.bashrc 
# copy ads ros into ws
COPY /src $CATKIN_WS/src

### build msgs 
RUN /bin/bash -c '. /opt/ros/${ROS_DISTRO}/setup.bash; cd ${CATKIN_WS}; catkin_make --pkg pcl_msgs pb_msgs autoware_msgs mobileye_msgs ibeo_msgs nmea_msgs '                   
### build ros nodes 
RUN /bin/bash -c '. /opt/ros/${ROS_DISTRO}/setup.bash; cd ${CATKIN_WS}; catkin_make '

# copy ros scripts
COPY /script $CATKIN_WS/scripts 

# run ros shell
WORKDIR ${CATKIN_WS}/scripts 

```


#### ros IP envs

set `ROS_IP` on all involved containers to their IP, and set `ROS_MASTER_URI` to the IP of the roscore container. That would avoid the DNS problem. understand [ros environment variables](http://wiki.ros.org/ROS/EnvironmentVariables)

* $ROS_ROOT :   set the location whre the ROS core packages are installed 

* $ROS_MASTER_URI :  a required setting that tells nodes where they can locate the master

* $ROS_IP/$ROS_HOSTNAME : sets the declared network address of a ROS node


#### get docker container's IP 

```
docker inspect -f "{{ .NetworkSettings.Networks.<network_name>.IPAddress }}" <container_name||container_id> 

``` 

* network_name: e.g. host, bridge, ingress e.t.c.



with [docker host net](https://docs.docker.com/network/host/), then the container doesn't have its own IP address allocated, but the application is available on the host's IP address with customized port.

 
#### run roscore in docker and talk to rosnodes at host 

* start roscore from docker container as following :

```
sudo docker run -it --net host ads_ros /bin/bash
roscore 
``` 

* start other ros nodes at host 

```
rosnode list  ## >>>  /rosout 
source $ROS_PACKAGE/setup.sh
rosrun rtk_sensor rtk_sensor   ### run successfully 
``` 

how to understand ?  once the docker container start with `host network`, the `roscore` run inside docker, is same as run in the host machine !! 


#### ads ros in docker talk to lgsvl in another docker with HOST network 

* once we start ads ros docker as following: 

```
sudo docker run -it --net host ads_ros /bin/bash
roscore 
``` 

* start lgsvl in docker: 

```
#! /usr/bin/env bash

xhost + 

sudo nvidia-docker run -it  -p 8080:8080  -e DISPLAY=unix$DISPLAY --net host -v /tmp/.X11-unix:/tmp/.X11-unix lgsvlsimulator /bin/bash

```

then access webUI in host machine, and add `host: 10.20.181.132` in `Clusters` page, and  add `10.20.181.132:9090` for Selected Vehicles. as lgsvl is also in `host network`. so these two docker can communicate through ros well !! 


#### ads ros container talk to lgsvl container with ROS_IP


since lgsvl will run in docker swarm env, we can't depend on `host network`, which requires $ROS_IP env. the following test is in one host machine. 


* in host terminal 

```
export ROS_MASTER_URI=http://192.168.0.10:11311
export ROS_HOSTNAME=192.168.0.10
export ROS_IP=192.168.0.10   

roscore 

``` 

* in ads ros docker 

```
sudo docker run -it \ 
     --env ROS_MASTER_URI=http://10.20.181.132:11311 \ 
     --env ROS_IP=10.20.181.132 \ 
     ads_ros /bin/bash

rosnod list 

``` 

however, when start `roscore` in docker, it reports:

```
Unable to contact my own server at [http://10.20.181.132:33818/].
This usually means that the network is not configured properly.

A common cause is that the machine cannot ping itself.  Please check
for errors by running:

	ping 10.20.181.132

``` 

if checking the IP address inside the docker container by `ifconfig`, which is `172.17.0.3`, which does make sense that the container can't talk to `10.20.181.132`, which means we can't assign a special IP address for a docker container. 


so reset in the docker container as:

```
export ROS_MASTER_URI=http://172.17.0.3:11311
export ROS_HOSTNAME=172.17.0.3
```

and actually, the host terminal can talk to the ads ros container directly, with no need to set `$ROS_HOSTNAME` & `$ROS_MASTER_URI` specially; as well as another docker container in this host machine, e.g. lgsvl. 


a little bit knowledge about docker network. so each docker container does have an virtual IP, e.g. 172.17.0.1. while if run the docker image with `host network`, there is no special container IP, but the container directly share the IP of the host machine. as multi docker containers run in the same host machine, even without `host network`, they are in the same network range, so they can communicate to each other. additionaly for `ros_master`, which may requires to add `$ROS_HOSTNAME` & `$ROS_MASTER_URI`.


* start lgsvl in another docker 

```
#! /usr/bin/env bash

xhost + 

sudo nvidia-docker run -it \ 
     -p 8080:8080 \  
     -e DISPLAY=unix$DISPLAY \ 
     -v /tmp/.X11-unix:/tmp/.X11-unix \ 
     --env ROS_MASTER_URI=http://172.17.0.3:11311  \ 
     --env ROS_HOSTNAME=172.17.0.3   
     lgsvlsimulator /bin/bash
 
```

so far, we have host ads ros in one docker, and lgsvl in another docker, and they are in the same machine, and they can talk to each other. the next thing is to put ads ros and lgsvl in one image.





## refer

[listening to ROS messages in docker containers](https://answers.ros.org/question/244424/listening-to-ros-messages-in-docker-containers/)

[exposing ROS containers to host machine](https://answers.ros.org/question/228292/exposing-ros-containers-to-host-machine/)

[why you need IP address of Docker container](https://takacsmark.com/how-to-get-docker-container-ip-address/)


[catkin_make not found in dockerfile](https://answers.ros.org/question/312577/catkin_make-command-not-found-executing-by-a-dockerfile/)














