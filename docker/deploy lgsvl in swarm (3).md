
## background

previously tried to [run Vulkan in virtual display](), which failed as I understand virtual display configure didn't fit well with Vulkan. so this solution is direct display to allow each node has plugged monitor(which is called **PC cluster**). for future in cloud support, current solution won't work. and earlier, also tried to [deploy lgsvl in docker  swarm](), which so far can work with Vulkan as well, after a little bit [understand X11]().


a few demo test can run as followning:


#### deploy glxgears/OpenGL in PC cluster

```
export DISPLAY=:0 
xhost + 
sudo docker service create --name glx --generic-resource "gpu=1" --constraint 'node.role==manager'  --env DISPLAY --mount src="X11-unix",dst="/tmp/.X11-unix" --mount src="tmp",dst="/root/.Xauthority"  --network host  192.168.0.10:5000/glxgears   

```

#### deploy vkcube/Vulkan in PC cluster 

```
export DISPLAY=:0 
xhost +  
sudo docker service create --name glx --generic-resource "gpu=1" --constraint 'node.role==manager'  --env DISPLAY --mount src="X11-unix",dst="/tmp/.X11-unix" --mount src="tmp",dst="/root/.Xauthority"  --network host  192.168.0.10:5000/vkcube   

```


#### deploy service with "node.role==worker" 

```
export DISPLAY=:0
xhost + 
sudo docker service create --name glx --generic-resource "gpu=1" --constraint 'node.role==worker'  --env DISPLAY --mount src="tmp",dst="/root/.Xauthority"  --network host  192.168.0.10:5000/glxgears

```

#### deploy service in whole swarm

```
xhost + 
export DISPLAY=:0 
sudo docker service create --name glx --generic-resource "gpu=1" --replicas 2  --env DISPLAY --mount src="tmp",dst="/root/.Xauthority"  --network host  192.168.0.10:5000/vkcube 
```

which deploy vkcube service in both manager and worker node:


	overall progress: 2 out of 2 tasks 
	1/2: running   [==================================================>]	 
	2/2: running   [==================================================>] 
	verify: Service converged 



#### understand .Xauthority

as docker service can run with `--mount` arguments, which give the first try to copy `.Xauthority` to manager node, but `.X11-unix` is not copyable, which is not a normal file, but a socket.

in `docker service create`, when create a OpenGL/vulkan service in one remote worker node, and using `$DISPLAY=:0`, which means the display happens at the remote worker node. so in this way, the remote worker node is played the `Xserver` role; and since the vulkan service is actually run in the remote worker node, so the remote worker node is `Xclient` ? 

assuming the lower implement of `docker swarm service`is based on `ssh`, then when the manager node start the service, it will build the ssh tunnel to the remote worker node, and with the $DISPLAY variable as null; even if the docker swarm can start the ssh tunnel with `-X`, which by default, will use the manager node's `$DISPLAY=localhost:10.0`

`Xauthority cookie` is used to grant access to Xserver, so first make sure which machine is the Xserver, then the Xauthority should be included in that Xserer host machine. a few testes: 

```
ssh in worker: echo $DISPLAY -->  localhost:10.0

xeyes --> display in master monitor 

ssh in worker: xauth list --> {worker/unix:0  MIT-MAGIC-COOKIE-1  19282b0a651789ed27950801ef6f1441; worker/unix:10  MIT-MAGIC-COOKIE-1  a6cbe81637207bf0c168b3ad20a9267a }

in master: xauth list --> { ubuntu/unix:1  MIT-MAGIC-COOKIE-1  ee227cb9465ac073a072b9d263b4954e; ubuntu/unix:0  MIT-MAGIC-COOKIE-1  75893fb66941792235adba22362c4a6f; ubuntu/unix:10  MIT-MAGIC-COOKIE-1  785f20eb0ade772ceffb24eadeede645 }

```

so which cookie is is for this $DISPLAY ? it shouldb be the one on `ubuntu/unix:10`;

```
ssh in worker:  export DISPLAY=:0
xeyes  --> display in worker monitor 
```
then it use the cookie:  `worker/unix:0`.


#### deploy lgsvl service in swarm

```
xhost + 
export DISPLAY=:0
sudo docker service create --name lgsvl --generic-resource "gpu=1" --replicas 2  --env DISPLAY --mount src="tmp",dst="/root/.Xauthority"  --network host --publish published=8080,target=8080  192.168.0.10:5000/lgsvl 

```

which gives:


	overall progress: 0 out of 2 tasks 
	1/2: container cannot be disconnected from host network or connected to host network
	2/2: container cannot be disconnected from host network or connected to host network


basically, the service is deployed in `ingress network` by default, but as well, the service is configured with `host network`. so it conflict.

## swarm network 


![image](https://docs.docker.com/engine/swarm/images/ingress-lb.png)


the [routing mesh](https://docs.docker.com/engine/swarm/services/#publish-a%20services-ports-using-the-routing-mesh) is the default internal balancer in swarm network; the other choice is to [deploy serivce directly on the node](https://docs.docker.com/engine/swarm/services/#publish-a-services-ports-directly-on-the-swarm-node), namely `bypassing routing mesh`, which ask the service run in `global mode` and with pubished port setting as `mode=host`, which should be the same as `--network host` in `replicas mode`. 

the limitation of bypassing routing mesh, is only one task on one node, and access the published port can only require the service from this special node, which doesn' make sense in cloud env.

 
```
docker service create \
     --mode global \
     --publish mode=host,target=80,published=8080 \
     --generic-resource "gpu=1"  \
     --env DISPLAY  \
     --mount src="tmp",dst="/root/.Xauthority"  \
     --mount src="X11-unix",dst="/tmp/.X11-unix"  \
     --network host  \
     --name lgsvl \
     lgsvl:latest
 
```

tips: --mount src="X11-unix",dst="/tmp/.X11-unix" is kind of cached. so once docker image has ran in worker node, then it doesn't need to pass this parameter again, but once worker node restart, it need this parameter again


in summary about swarm netowrk, the routing mesh should be the right solution for cloud deployment. so how to bypass `--network host` ? 


the reason of `host network` is the lgsvl server and webUI can works in same host; if not, there is kind of cross-domain security failures, which actually is another topic, namely, how to host lgsvl and webUI/React in different hosts.

need some study recently.

 














