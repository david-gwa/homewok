## backround 


[previously](), we had test to run ads ros in one docker container, and lgsvl simulator in another docker container. once they are hosted in the same host machine, the ADS ros nodes and lgsvl can communicate well. based on this work, now it's the time to integrate ADS ros nodes into the lgsvl docker.


the basic idea of how to combine multi docker images into one, is [use multistage-build](https://docs.docker.com/develop/develop-images/multistage-build/), which I call "image level integration".

#### image level integration 

basically we have both `ads_ros` image and `lgsvlsimulator` image already, and there are a few components from `ads_ros` can be imported to `lgsvlsimulator` container: 

```
FROM ads_ros:latest  AS ADS
FROM lgsvlsimulator:latest
RUN mkdir /catkin_ws
COPY --from=ADS /root/catkin_ws  /catkin_ws
COPY --from=ADS /opt/ros /opt/ros 
CMD ["/bin/bash"]

```

the problem of `image level integration`, it actually miss some system level components: `/etc/apt/sources.list.d/ros-latest.list`, which then can't update ros modules; other components, e.g. which are installed during building `ads_ros` image by `apt-get install`, which are go the system lib path, which of course can distinct out, and copy to `lgsvlsimulator`, but which is no doubt tedious and easy to miss some components.


#### component level integration 


as `ads_ros` is really indepent to `lgsvlsimulator`, so another way is use `lgsvlsimulator` as base image, then add/build `ros` component and `ads_ros` compnents inside.

```
FROM ros:kinetic  AS ROS
# or to install ros from source directly 
# http://wiki.ros.org/kinetic/Installation/Ubuntu

FROM lgsvlsimulator:latest
RUN mkdir -p /catkin_ws/src
COPY --from=ROS /opt/ros /opt/ros 
COPY --from=ROS /etc/apt/sources.list.d/ros1-latest.list /etc/apt/sources.list.d/ros1-latest.list
# ADD ros key
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
## -------- install ads ros packages in lgsvlsimulator container ------------ ##
ENV CATKIN_WS=/catkin_ws
ENV ROS_DISTRO=kinetic
## https://docs.ros.org/api/catkin/html/user_guide/installation.html
RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        build-essential \
        apt-utils \
        ca-certificates \ 
        psmisc \
        cmake \
        python-catkin-pkg \ 
        ros-${ROS_DISTRO}-catkin  \ 
        ros-${ROS_DISTRO}-tf  \
        ros-${ROS_DISTRO}-turtlesim \
        ros-${ROS_DISTRO}-rosbridge-suite \
        iputils-ping \   
        net-tools 
# RUN source ~/.bashrc 
# copy ads ros into ws
COPY /ads_ros/src $CATKIN_WS/src
### build msgs 
RUN /bin/bash -c '. /opt/ros/${ROS_DISTRO}/setup.bash; cd ${CATKIN_WS}; catkin_make --pkg pcl_msgs autoware_msgs nmea_msgs '                   
### build ros nodes 
RUN /bin/bash -c '. /opt/ros/${ROS_DISTRO}/setup.bash; cd ${CATKIN_WS}; catkin_make '
# copy ros scripts
COPY /ads_ros/script_docker $CATKIN_WS/script
###--------finished ads ros package -------------- ### 
CMD ["/bin/bash"]

``` 


## runtime issue 

with the dockerfile above, we can build the docker image which include both lgsvl and ads ros. one runtime issue is due to lgsvl scenario is run with `python3`, while our ads ros, especially `ros_bridge_launch` is based on `python2`. so need some trick to add `python2` at `$PATH` before `python3` when launch `ros_bridge`, then exchange back.




















