

## background 

previously, I tried to deploy lgsvl by docker compose v3, which at first sounds promising, but due to lack of runtime support, which doesn't work any way.  this is another to deploy lgsvl with `docker service create --generic-resource`.


## docker service options

[docker service](https://docs.docker.com/engine/swarm/services/) support a few common [options](https://docs.docker.com/engine/reference/commandline/service_create/)


* `--workdir` is the working directory inside the container 

* `--args` is used to update the command the service runs 

* `--publish <Published-Port>:<Service-Port>` 

* `--network` 

* `--mount` 

* `--mode` 

* `--env` 

* [--config](https://docs.docker.com/engine/swarm/configs/)


## docker service create with generic-resource

#### generic-resource 

create services requesting [generic resources](https://docs.docker.com/v17.12/edge/engine/reference/commandline/service_create/#specify-isolation-mode-windows) is supported well:

```script
$ docker service create --name cuda \
                        --generic-resource "NVIDIA-GPU=2" \
                        --generic-resource "SSD=1" \
                        nvidia/cuda
```

tips: need to understand what is [generic-resource "NVIDIA-GPU=2"]



als supported in [docker compose v3.5](https://stackoverflow.com/questions/49141284/docker-swarm-generic-device-resource-connection):

```
       generic_resources:
           - discrete_resource_spec:
              kind: 'gpu'
              value: 2
```


`--generic-resource` has the ability to access GPU in service, a few blog topics:

* [GPU Orchestration Using Docker](https://codingsans.com/blog/gpu-orchestration-using-docker)

* [access gpus from swarm service](http://cowlet.org/2018/05/21/accessing-gpus-from-a-docker-swarm-service.html)


#### first try

follow [accessing GPUs from swarm service](http://cowlet.org/2018/05/21/accessing-gpus-from-a-docker-swarm-service.html). install [nvidia-container-runtime](https://github.com/NVIDIA/nvidia-container-runtime) and install `docker-compose`, and run the following script:


```script
export GPU_ID=`nvidia-smi -a | grep UUID | awk '{print substr($4,0,12)}'`
sudo mkdir -p /etc/systemd/system/docker.service.d
cat EOF | sudo tee --append /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fdd:// --default-runtime=nvidia --node-generic-resource gpu=${GPU_ID}
EOF
sudo sed -i 'swarm-resource = "DOCKER_RESOURCE_GPU"' /etc/nvidia-container-runtime/config.toml
sudo systemctl daemon-reload
sudo systemctl start docker

```

to understand supported dockerd options, can check [here](https://github.com/docker/cli/blob/master/docs/reference/commandline/dockerd.md), then run the test as: 

	docker service create --name vkcc --generic-resource "gpu=0" --constraint 'node.role==manager' nvidia/cudagl:9.0-base-ubuntu16.04

	docker service create --name vkcc --generic-resource "gpu=0" --env DISPLAY=unix:$DISPLAY --mount src="X11-unix",dst="/tmp/.X11-unix" --constraint 'node.role==manager' vkcube 


which gives the errors:

	1/1: no suitable node (1 node not available for new tasks; insufficient resourc… 
	1/1: no suitable node (insufficient resources on 2 nodes) 


if run as, where `GPU-9b5113ed` is the physical GPU ID in node:

	docker service create --name vkcc --generic-resource "gpu=GPU-9b5113ed" nvidia/cudagl:9.0-base-ubuntu16.04

which gives the error: 

	invalid generic-resource request `gpu=GPU-9b5113ed`, Named Generic Resources is not supported for service create or update


as I think these errors are due to swarm cluster can't recognized this GPU resource, which is configured in `/etc/nvidia-container-runtime/config.toml`


#### second try

as mentioined in [GPU orchestration using Docker](https://codingsans.com/blog/gpu-orchestration-using-docker), another change can be done:


	ExecStart=/usr/bin/dockerd -H unix:///var/run/docker.sock --default-runtime=nvidia --node-generic-resource gpu=${GPU_ID}


which fixes the `no suitable node` issue, but start container failed: OCI..

```script
root@ubuntu:~# docker service ps vkcc  
ID                  NAME                IMAGE                                NODE                DESIRED STATE       CURRENT STATE           ERROR                              PORTS
orhcaxyujece        vkcc.1              nvidia/cudagl:9.0-base-ubuntu16.04   ubuntu              Ready               Ready 3 seconds ago                                        
e001nd557ka6         \_ vkcc.1          nvidia/cudagl:9.0-base-ubuntu16.04   ubuntu              Shutdown            Failed 3 seconds ago    "starting container failed: OC…"   

```

check daemon log with ` sudo journalctl -fu docker.service`, which gives:

```
Nov 21 13:07:12 ubuntu dockerd[1372]: time="2019-11-21T13:07:12.089005034+08:00" level=error msg="fatal task error" error="starting container failed: OCI runtime create failed: unable to retrieve OCI runtime error (open /run/containerd/io.containerd.runtime.v1.linux/moby/9eee7ac30a376ee8f59704f7687455bfb163e5ea3dd6d09d24fbd69ca2dfaa4e/log.json: no such file or directory): nvidia-container-runtime did not terminate sucessfully: unknown" module=node/agent/taskmanager node.id=emzw1f9293rwdk97ki7gfqq1q service.id=qdma7vr1g519lz9hx2y1fen9o task.id=ex1l4wy61kvughns5uzo6qgxy

```


#### third try 


following [issue #141](https://github.com/NVIDIA/nvidia-docker/issues/141#issuecomment-356458450)


```
nvidia-smi -a | grep UUID | awk '{print "--node-generic-resource gpu="substr($4,0,12)}' | paste -d' ' -s
sudo systemctl edit docker

[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// --default-runtime=nvidia <resource output from the above>

```

and run: 

		docker service create --name vkcc --generic-resource "gpu=1" --env DISPLAY --constraint 'node.role==manager' nvidia/cudagl:9.0-base-ubuntu16.04


it works !!! with output `verify: Service converged `. However, when test image with `vucube` or `lgsvl` it has errors:

```
error msg="pulling image failed" error="pull access denied for vkcube, repository does not exist or may require 'docker login'"

Nov 21 19:33:20 ubuntu dockerd[52334]: time="2019-11-21T19:33:20.467968047+08:00" level=error msg="fatal task error" error="task: non-zero exit (1)" module=node/agent/taskmanager node.id=emzw1f9293rwdk97ki7gfqq1q service.id=spahe4h24fecq11ja3sp8t2cn task.id=uo7nk4a3ud201bo9ymmlpxzr3

```

the regsitry error can be fixed, by push the image to local registry. and to debug the `non-zero exit (1)` :


```
docker service  ls    #get the dead service-ID

docker [service] inspect  r14a68p6v1gu  # check 

docker ps -a  # find the dead container-ID 

docker logs  ff9a1b5ca0de   # check the log of the failure container

``` 

it gives: `Cannot find a compatible Vulkan installable client driver (ICD)` 

I had an issue at [gitlab/nvidia-images](https://gitlab.com/nvidia/container-images/vulkan/issues/2)



#### generic-resource support discussion 

[moby issue 33439: add support for swarmkit generic resources](https://github.com/moby/moby/issues/33439)

* how to advertise Generic Resources(republish generic resources)
* how to request Generic Resources 

[nvidia-docker issue 141: support for swarm mode in Docker 1.12](https://github.com/NVIDIA/nvidia-docker/issues/141)

[docker issue 5416: Add Generic Resources](https://github.com/docker/docker.github.io/pull/5416)

**Generic resources**

[Generic resources](https://github.com/RenaudWasTaken/docker.github.io/blob/master/compose/compose-file/index.md) are a way to select the kind of nodes your task can land on.

In a swarm cluster, nodes can advertise Generic resources as discrete values or as named values such as SSD=3 or GPU=UID1, GPU=UID2.

The Generic resources on a service allows you to request for a number of these Generic resources advertised by swarm nodes and have your tasks land on nodes with enough available resources to statisfy your request.

If you request Named Generic resource(s), the resources selected are exposed in your container through the use of environment variables. E.g: DOCKER_RESOURCE_GPU=UID1,UID2

You can only set the generic_resources resources' reservations field.


[overstack: schedule a container with swarm using GPU memory as a constraint](https://stackoverflow.com/questions/40172594/schedule-a-container-with-docker-swarm-using-gpu-memory-as-a-constraint)


[label swarm nodes](https://docs.docker.com/v17.12/datacenter/ucp/2.2/guides/admin/configure/add-labels-to-cluster-nodes/)

	$ docker node update --label-add <key>=<value> <node-id>


* [compose issue #6691](https://github.com/docker/compose/issues/6691)
* [docker-nvidia issue #141](https://github.com/NVIDIA/nvidia-docker/issues/141)



#### SwarmKit 

[swarmkit](https://github.com/docker/swarmkit) also support [GenericResource](https://github.com/docker/swarmkit/blob/master/design/generic_resources.md), please check [design doc](https://github.com/docker/swarmkit/blob/master/design/generic_resources.md#use-cases)

```shell
$ # Single resource
$ swarmctl service create --name nginx --image nginx:latest --generic-resources "banana=2"
$ # Multiple resources
$ swarmctl service create --name nginx --image nginx:latest --generic-resources "banana=2,apple=3"
```

	./bin/swarmctl service create --device /dev/nvidia-uvm --device /dev/nvidiactl --device /dev/nvidia0 --bind /var/lib/nvidia-docker/volumes/nvidia_driver/367.35:/usr/local/nvidia --image nvidia/digits:4.0 --name digits


swarmkit add support [devices option](https://github.com/docker/swarmkit/issues/1244)



## refer
[manage swarm service with config](https://stackoverflow.com/questions/51398808/how-to-manage-docker-swarm-service-configuration)

[UpCloud: how to configure Docker swarm](https://upcloud.com/community/tutorials/how-to-configure-docker-swarm/)

[Docker compose v3 to swarm cluster](https://codefresh.io/docker-tutorial/deploy-docker-compose-v3-swarm-mode-cluster/)

[deploy docker compose services to swarm](https://blog.couchbase.com/deploy-docker-compose-services-swarm/)

[docker deploy doc](https://docs.docker.com/v17.12/edge/engine/reference/commandline/deploy/)

[alexei-led github](https://github.com/alexei-led/swarm-mac/blob/master/init_swarm.sh)

[Docker ARG, ENV, .env -- a complete guide](https://vsupalov.com/docker-arg-env-variable-guide/)







