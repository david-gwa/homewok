

## Xorg 

Xorg is client-server architecture, including Xprotocol, Xclient, Xserver. Linux itself has no graphics interface, all GUI apps in Linux is based on X protcol.

Xserver used to manage the Display device, e.g. monitor, Xserver is responsible for displaying, and send the device input(e.g. keyboard click) to Xclient.

Xclient, or X app, which includes grahics libs, e.g. OpenGL, Vulkan e.t.c

 
#### xauthority 

Xauthority file can be found in each user home directory and is used to store credentials in cookies used by xauth for authentication of X sessions. Once an X session is started, the cookie is used to authenticate connections to that specific display. You can find more info on X authentication and X authority in the xauth man pages (type man xauth in a terminal). if you are not the owner of this file you can't login since you can't store your credentials there.

when `Xorg` starts, `.Xauthority` file is send to Xorg, review this file by `xauth -f ~/.Xauthority` 

ubuntu@ubuntu:~$ xauth -f ~/.Xauthority 
Using authority file /home/wubantu/.Xauthority
xauth> list 
ubuntu/unix:1  MIT-MAGIC-COOKIE-1  ee227cb9465ac073a072b9d263b4954e
ubuntu/unix:0  MIT-MAGIC-COOKIE-1  71cdd2303de2ef9cf7abc91714bbb417
ubuntu/unix:10  MIT-MAGIC-COOKIE-1  7541848bd4e0ce920277cb0bb2842828

`Xserver` is the host who will used to display/render graphics, and the other host is `Xclient`. if Xclient is from remote host, then need configure $DISPLAY in `Xserver`. To display X11 on remote Xserver,  need to copy the .Xauthority from Xserver to Xclient machine, and export $DISPLAY and $XAUTHORITY

```
 export DISPLAY={Display number stored in the Xauthority file}
 export XAUTHORITY={the file path of .Xauthority}
```

#### xhost

[Xhost](https://www.linuxidc.com/Linux/2012-11/74874.htm) is used to grant access to Xserver (on your local host), by default, the local client can access the local Xserer, but any remote client need get granted first through Xhost. taking an example, when ssh from hostA to hostB, and run `glxgears` in this ssh shel. for grahics/GPU resources,  hostA is used to display, so hostA is the Xserver.


#### x11 forwarding 

when Xserver and Xclient are in the same host machine, nothing big deal. but Xserver, Xclient can totally be on different machines, as well as Xprotocol communication between them. this is how SSH -X helps to run the app in Xclient, and display in Xserver, which needs `X11 Forwarding`.


![image](http://www.ipaomi.com/wp-content/uploads/2017/11/x_server_client_remote.gif)


#### test benchmark 

```
ssh 192.16.0.13
xeyes
```

#### /tmp/.X11-unix 

the X11(xorg) server communicates with client via some kind of reliable stream of bytes. 

A Unix-domain socket is like the more familiar TCP ones, except that instead of connecting to an address and port, you connect to a path. You use an actual file (a socket file) to connect.

	srwxrwxrwx 1 root root 0 Nov 26 08:49 X0

the `s` in front of the permissions, which means its a socket. If you have multiple X servers running, you'll have more than one file there.

is where X server put listening AF_DOMAIN sockets. 

#### DISPLAY device 

DISPLAY format: **hostname: displaynumber.screennumber**

hostname is the hostname or hostname IP of Xserver

displaynumber starting from 0
screennumber starting from 0


when using TCP(x11-unix protocol only works when Xclient and Xserver are in the same machine), displaynumber is the connection port number minus 6000; so if displaynumber is 0, namely the port is 6000. `DISPLAY` refers to a display device, and all graphics will be displayed on this device. 
by deafult,  Xserver localhost doesn't listen on TCP port. run: `sudo netstat -lnp | grep "6010" `, no return. [how to configure Xserver listen on TCP](https://askubuntu.com/questions/1143831/xserver-listen-on-tcp-ubuntu-19-04)


```
Add DisallowTCP=false under directive [security] in /etc/gdm3/custom.conf file. Now open file /etc/X11/xinit/xserverrc and change exec /usr/bin/X -nolisten tcp to exec /usr/bin/X11/X -listen tcp. Then restart GDM with command sudo systemctl restart gdm3. To verify the status of listen at port 6000, issue command ss -ta | grep -F 6000. Assume that $DISPLAY value is :0.
```

#### virtual DISPLAY device 

[creating a virtual display/monitor](https://bbs.archlinux.org/viewtopic.php?id=180904)
[add fake display when no Monitor is plugged in](https://bbs.archlinux.org/viewtopic.php?id=180904)


## Xserver broadcast 

the idea behind is to stand in one manager(Xserver) machine, and send command to a bunch of worker(Xclient) machines. the default way is all Xclient will talk to Xserver, which eat too much GPU and network bandwith resources on manager node. so it's better that each worker node will do the display on its own. and if there is no monitor on these worker nodes, they can survive with virtual display.

#### xvfb

[xvfb](http://manpages.ubuntu.com/manpages/xenial/man1/xvfb-run.1.html) is the virtual Xserver solution, but doesn't run well(need check more)

#### nvidia-xconfig 

[configure X server to work headless as well with any monitor connected](https://devtalk.nvidia.com/default/topic/585014/how-to-configure-x-server-to-work-headless-as-well-with-any-monitor-connected-/)


#### unity headless 



## env setup

to test with docker, vulkan, ssh, usually need the following packages: 

#### vulkan dev env  

	sudo add-apt-repository ppa:graphics-drivers/ppa
	sudo apt upgrade
	apt-get install libvulkan1 vulkan vulkan-utils 
	sudo apt install vulkan-sdk 

#### nvidia env 

	install nvidia-driver, nvidia-container-runtime
	install mesa-utils  #glxgears

#### docker env 

	install docker 


## run glxgear/vkcube/lgsvl in docker through ssh tunnel

there is a very nice blog: [Docker x11 client via SSH](https://dzone.com/articles/docker-x11-client-via-ssh), disccussed the arguments passing to the following samples


#### run glxgear 

glxgear is OpenGL benchmark test. 

```
ssh -X -v abc@192.168.0.13
sudo docker run --runtime=nvidia -ti --rm -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v "$HOME/.Xauthority:/root/.Xauthority" --net=host 192.168.0.10:5000/glxgears

```

if seting $DISPLAY=localhost:10.0 , then the gears will display at master node(ubuntu)

if setting $DISPLAY=:0,  then the gears will display at worker node(worker)

and w/o `/tmp/.X11-unix` it works as well. 


#### run vkcube 

vkcube is Vulkan benchmark test.

```
ssh -X -v abc@192.168.0.13
export DISPLAY=:0
sudo docker run --runtime=nvidia -ti --rm -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v "$HOME/.Xauthority:/root/.Xauthority" --net=host  192.168.0.10:5000/vkcube
```

in this way, vkcube is displayed in worker node(namely, using worker GPU resource), manager node has no burden at all. 

if `$DISPLAY=localhost:10.0`, to run vkcube, give errors:

	No protocol specified
	Cannot find a compatible Vulkan installable client driver (ICD).
	Exiting ...

looks vulkan has limitation.



#### run lgsvl

```
export DISPLAY=:0
sudo docker run --runtime=nvidia -ti --rm -p 8080:8080 -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v "$HOME/.Xauthority:/root/.Xauthority" --net=host  192.168.0.10:5000/lgsvl  /bin/bash 
./simulator 

```

works well!



## refer

[wiki: Xorg/Xserver](https://www.x.org/wiki/XServer/)
[IBM study: Xwindows](https://www.ibm.com/developerworks/cn/linux/l-cn-xwin/index.html)
[cnblogs: run GUI in remote server](https://www.cnblogs.com/ipaomi/p/7830778.html)
[xorg.conf in ubuntu](https://wiki.ubuntu.com/X/Config)
[configure Xauthority](https://docs.citrix.com/en-us/linux-virtual-delivery-agent/current-release/configuration/configure-xauthority.html)
[X11 forwarding of a GUI app running in docker](https://stackoverflow.com/questions/44429394/x11-forwarding-of-a-gui-app-running-in-docker)
[cnblogs: Linux DISPLAY skills](https://www.cnblogs.com/kevin-boy/p/3223404.html)
[nvidia-runtime-container feature: Vulkan support](https://github.com/NVIDIA/nvidia-docker/issues/631)




