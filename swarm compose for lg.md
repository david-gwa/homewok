

### micro-services

the whole appliations decomposed as a bunch of micro-service, as components.




####  check  cluster

```shell
 sudo docker node ls 
```

#### create service 

```shell

	docker service create [options] image
```

[go micro-service](https://segmentfault.com/a/1190000014961997)
[go micro-service2](https://segmentfault.com/a/1190000014924259)

#### create service with compose.yaml

 `docker service create` can deploy only one service by once;  `compose.yml` allow to luanch and deploy multi service at once


```shell
	
docker stack deploy -c docker-compose.yml  parent_service_name

docker stack ls 

docker stack down

```

### docker compose 

[tencent yun](https://cloud.tencent.com/developer/news/121227)
使用docker本地服务配置和部署工具来调试和测试多容器应用。
将数据库放在一个容器中，将Web应用程序放在另一个容器中，并且可以将它们全部缩放，管理，重新启动并独立换出。 但是开发和测试一个多容器应用程序并不像一次使用一个容器。
docker compose接收一个特殊格式的描述符文件，将应用程序从多个容器中组装出来，并在单个主机上一起运行。

最小的Docker Compose应用程序由三个组件组成：

1. 要构建的每个容器镜像的Dockerfile。

2. Docker Compose将用于从这些镜像启动容器并配置其服务的YAML文件docker-compose.yml。

3. 构成应用程序本身的文件。



```shell

docker-compose build

docker-compose up  #启动应用中所有容器

docker-compose down #取消容器运行

docker-compose up --scale  

docker-compose  start/restart/stop/pause

```

### how compose works



### compose.yml file 

```shell 

  collect:
    build:
      context: .
    image: lgsvl/lanefollowing:latest
    container_name: lanefollowing_collect
    volumes:
      - .:/lanefollowing
    environment:
      - CUDA_CACHE_PATH=/lanefollowing/.nv
    runtime: nvidia
    network_mode: host
    init: true
    privileged: true
command: /lanefollowing/scripts/collect.sh

```

depends_on   # manage depends order
 
build: 


image:

container_name:

volumes:

network_mode:

init:

privileged:

command:

environment: 


### swtich docker engine mode

sudo docker node demote  nodeID
sudo docker swarm leave --force # 


#### test with compose-test
[official](https://docs.docker.com/compose/gettingstarted/)


### docker run failed
ERROR: for second-ros  Cannot start service second-ros: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:430: container init caused \"write /proc/self/attr/keycreate: invalid argument\"": unknown


https://github.com/opencontainers/runc/issues/2030


### test with second-ros

	docker-compose up second-ros



#### systemctl 

	systemctl list-unit-files  --type=service 



#### unintall k8s
kubeadm reset
sudo apt-get purge kubeadm kubectl kubelet kubernetes-cni kube*   
sudo apt-get autoremove  
sudo rm -rf ~/.kube

rm  /etc/apt/sources.list.d/kubernetes.list 


error return:

dpkg: error processing package libc-bin (--configure):
 subprocess installed post-installation script returned error exit status 2
Errors were encountered while processing:
 libc-bin


sol:  


sudo -i
rm /var/cache/ldconfig/aux-cache 
/sbin/ldconfig 

sudo apt-get --reinstall install libc-bin 





#### uninstall docker-compose

 sudo rm  /usr/local/bin/docker-compose 


### selinux 

set back to "enable"

https://docs.fedoraproject.org/en-US/Fedora/13/html/Security-Enhanced_Linux/sect-Security-Enhanced_Linux-Working_with_SELinux-Enabling_and_Disabling_SELinux.html


#### swapon 

### uninstall yum

dpkg (subprocess): unable to execute installed post-installation script (/var/lib/dpkg/info/libc-bin.postinst): Permission denied
dpkg: error processing package libc-bin (--configure):
 subprocess installed post-installation script returned error exit status 2
Errors were encountered while processing:
 libc-bin
E: Sub-process /usr/bin/dpkg returned an error code (1)


docker: Error response from daemon: mkdir /var/lib/docker/overlay2/90dec0fd2adf909d3bf49373d26905eb25bde459687d0113cae822a2f5263f5e-init/merged/sys: permission denied.

### uninstall docker 

 sudo apt-get purge docker-engine
sudo apt-get autoremove --purge docker-engine
rm -rf /var/lib/docker

Error:

dpkg (subprocess): unable to execute installed post-installation script (/var/lib/dpkg/info/libc-bin.postinst): Permission denied


### the package system is broken 
Errors were encountered while processing:
 libc-bin





### clean  /var/lib/docker/overlay2/ ...


[docker system prune](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes)






### docker compose vs k8s

selinux for k8s

apparmor for docker compose 



##  docker-compose lg 



docker: Error response from daemon: Unknown runtime specified nvidia.

sol: sudo systemctl restart docker 




### compose up build/collect


(base) ubuntu@ubuntu:~/zj/lanefollowing-master$ sudo docker-compose up build 
Creating lanefollowing_build ... done
Attaching to lanefollowing_build
lanefollowing_build | Starting >>> lane_following
lanefollowing_build | Finished <<< lane_following [0.96s]
lanefollowing_build | 
lanefollowing_build | Summary: 1 package finished [1.49s]
lanefollowing_build exited with code 0




ERROR: for collect  Cannot start service collect: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:430: container init caused \"process_linux.go:413: running prestart hook 0 caused \\\"error running hook: exit status 1, stdout: , stderr: exec command: [/usr/bin/nvidia-container-cli --load-kmods configure --ldconfig=@/sbin/ldconfig.real --device=all --compute --utility --require=cuda>=9.2 --pid=16123 /var/lib/docker/overlay2/83ada169eaefbabf0d1832b1c463c1e8f2ed038ae9574169e2b5d1980f2ba7f6/merged]\\\\nnvidia-container-cli: requirement error: unsatisfied condition: cuda >= 9.2\\\\n\\\"\"": unknown



##  compose 



#### figure out how to trigger lg-sim in docker-compose.yml 




almost using second-ros yml


 Unable to contact my own server at [http://ubuntu:38311/].

 add `ROS_MASTER_URI` & `ROS_IP` in `docker-compose.yml` 

second-ros    | Traceback (most recent call last):
second-ros    |   File "/root/catkin_ws/src/second_ros/scripts/second_ros.py", line 17, in <module>
second-ros    |     import second.core.box_np_ops as box_np_ops
second-ros    | ModuleNotFoundError: No module named 'second'


second-ros    | rviz::RenderSystem: error creating render window: OGRE EXCEPTION(2:InvalidParametersException): Window with name 'OgreWindow(0)' already exists in GLRenderSystem::_createRenderWindow at /build/ogre-1.9-mqY1wq/ogre-1.9-1.9.0+dfsg1/RenderSystems/GL/src/OgreGLRenderSystem.cpp (line 1057)



second-ros    | [ERROR] [1562921161.169244893]: Unable to create the rendering window after 100 tries.
second-ros    | [rviz-4] process has died [pid 119, exit code -11, cmd /opt/ros/kinetic/lib/rviz/rviz -d /root/catkin_ws/src/second_ros/config/second_ros.rviz __name:=rviz __log:=/root/.ros/log/782414de-a481-11e9-ab62-c8d9d22439df/rviz-4.log].

rviz-*.log: 
^[[33m[ WARN] [1562921161.124956111]: OGRE EXCEPTION(2:InvalidParametersException): Window with name 'OgreWindow(0)' already exists in GLRenderSystem::_createRenderWindow at /build/ogre-1.9-mqY1wq/ogre-1.9-1.9.0+dfsg1/RenderSystems/GL/src/OgreGLRenderSystem.cpp (line 1057)^[[0m







#### test with glx
root@ubuntu:~/.ros/log/782414de-a481-11e9-ab62-c8d9d22439df# apt-get install mesa-utils 


glxinfo

glxgears   ## output with no renderings ... 




### 

[run vs up](https://stackoverflow.com/questions/33066528/should-i-use-docker-compose-up-or-run)


### 
(base) ubuntu@ubuntu:~/zj/lg-sim$ sudo docker-compose  up lg-run 
WARNING: The UID variable is not set. Defaulting to a blank string.
WARNING: The PWD variable is not set. Defaulting to a blank string.
Recreating lg-run ... done
Attaching to lg-run
lg-run         | /root/run/lg_run.sh: line 3: xhost: command not found
lg-run         | sudo: unable to resolve host ubuntu: Connection timed out
lg-run         | sudo: nvidia-docker: command not found



root@ubuntu:/lg_bin# glxinfo -B  
name of display: :0
display: :0  screen: 0
direct rendering: Yes
OpenGL vendor string: NVIDIA Corporation
OpenGL renderer string: Quadro P2000/PCIe/SSE2
OpenGL core profile version string: 4.5.0 NVIDIA 384.130
OpenGL core profile shading language version string: 4.50 NVIDIA
OpenGL core profile context flags: (none)
OpenGL core profile profile mask: core profile

OpenGL version string: 4.5.0 NVIDIA 384.130
OpenGL shading language version string: 4.50 NVIDIA
OpenGL context flags: (none)
OpenGL profile mask: (none)

OpenGL ES profile version string: OpenGL ES 3.2 NVIDIA 384.130
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20



[glxgears no rendering](https://github.com/lgsvl/second-ros/issues/1)

[coreyryanhanson](https://github.com/coreyryanhanson/dockerfiles/tree/master/glxgears)


[alsa dummy sound card](https://github.com/cypress-io/cypress-docker-images/issues/52)


[sol on rassipberry](https://github.com/luxus/rpi-docker-shairport-sync/issues/3)

ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory

[refer2](https://stackoverflow.com/questions/46946788/alsa-lib-conf-c4528-snd-config-evaluate-function-snd-func-refer-returned-err)


[install gdb]: 

Debug info from gdb:

Could not attach to process.  If your uid matches the uid of the target
process, check the setting of /proc/sys/kernel/yama/ptrace_scope, or try
again as the root user.  For more details, see /etc/sysctl.d/10-ptrace.conf
/tmp/mono-gdb-commands.ilzZDn:1: Error in sourced command file:
ptrace: Operation not permitted.


[due to docker](https://stackoverflow.com/questions/19215177/how-to-solve-ptrace-operation-not-permitted-when-trying-to-attach-gdb-to-a-pro)


docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined




[glxgears no rendering in docker with net=host](https://github.com/NVIDIA/nvidia-docker/issues/421)



### run server-client app in docker

[refer1](https://stackoverflow.com/questions/55325612/cant-run-client-server-application-with-docker)


### access gpu in docker swarm
[refer](http://cowlet.org/2018/05/21/accessing-gpus-from-a-docker-swarm-service.html)


[docker swarm load balancing](https://www.jianshu.com/p/dba9342071d8)


### ros docker env

 1) attach the whole /simulator to docker container
 
 2) to run API,  need  lgsvl_api.whl

%% current, lgsvl_api.whl has error: lgsvl-0.0.0-py3.whl is not a valid wheel filename.

 
[install python3.7](https://stackoverflow.com/questions/51279791/how-to-upgrade-python-version-to-3-7)


	
