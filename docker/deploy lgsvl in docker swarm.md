

## Docker registry

### update docker daemon with insecure-registries

* modify `/etc/docker/daemon.json` in worker node: 

adding `  "insecure-registries": ["192.168.0.10:5000"]   `

* systemctl restart docker 

* start registry service in manager node 

```
$ docker service create --name registry --publish published=5000,target=5000 registry:2

``` 

access docker registry on both manager node and worker node :

```
$ curl http://192.168.0.10:5000/v2/   #on manager node 
$ curl http://192.168.0.10:5000/v2/   #on worker node 
```

`insecure registry` is only for test; for product, it has to with secure connection, check the official doc about [deploy a registry server](https://docs.docker.com/registry/deploying/)


### upload images to this local registry hub 

```
docker tag  stackdemo  192.168.0.10:5000/stackdemo
docker push  192.168.0.10:5000/stackdemo:latest
curl  http://192.168.0.10:5000/v2/_catalog

``` 

* on worker run: 

```
docker pull 192.168.0.10:5000/stackdemo 
docker run -p 8000:8000  192.168.0.10:5000/stackdemo  
```

the purpose of `local registry` is to build a local docker image file server, to share in the cluster server. 


## Deploy compose


### docker-compose build 

`docker-compose build` is used to build the images. 

`docker-compose up .` will run the image, if not exiting, will build the image first.


for lgsvl app, the running has a few parameters, so directly run `docker-compose up` will report `no protocol` error.


### run vkcube in docker-compose

docker-compose v2 does support `runtime=nvidia`, by appending the following to `/etc/docker/daemon.json`:

```
   "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
```

to run vkcube in compose by:

```
xhost +si:localuser:root
docker-compose up
```

the docker-compose.yml is :

```
version: '2.3'

services:
 vkcube-test:
  runtime: nvidia
  volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix 
  environment:
  - NVIDIA_VISIBLE_DEVICES=0 
  - DISPLAY
#  image: nvidia/cuda:9.0-base
  image: vkcube
#  build: . 
```

however, currently [composev3 doesn't support NVIDIA runtime](https://github.com/docker/compose/issues?utf8=%E2%9C%93&q=nvidia), who is required to run stack deploy. 


### support v3 compose with nvidia runtime 

as discussed at [#issue: support for NVIDIA GPUs under docker compose](https://github.com/docker/compose/issues/6691):

```
services:
  my_app:
    deploy:
      resources:
        reservations:
          generic_resources:
            - discrete_resource_spec:
                kind: 'gpu'
                value: 2
```


update [daemon.json](https://www.ipyker.com/2018/03/22/docker-daemon) with `node-generic-resources`, an official sample of [compose resource](https://github.com/docker/cli/blob/9a39a1/cli/compose/loader/full-example.yml#L71-L74) can be reviewed. but so far, it only reports error:

```
ERROR: The Compose file './docker-compose.yml' is invalid because:
services.nvidia-smi-test.deploy.resources.reservations value Additional properties are not allowed ('generic_resources' was unexpected
```


### deploy compose_V3 to swarm

[docker compose v3](https://docs.docker.com/compose/compose-file/) has two run options, if triggered by `docker-compose up`, it is in standalone mode, will all services in the stack is host in current node; if triggered through `docker stack deploy` and current node is the manager of the swarm cluster, the services will be hosted in the swarm. btw, `docker compose v2` only support standalone mode.


take an example from the official doc: [deploy a stack to swarm](https://docs.docker.com/engine/swarm/stack-deploy/):


```
docker service create --name registry --publish published=5000,target=5000 registry:2
docker-compose up -d
docker-compose ps
docker-compose down --volumes
docker-compose push #push to local registry
docker stack deploy
docker stack services stackdemo
docker stack rm stackdemo
docker service rm registry
```

after deploy `stackdemo` in swarm, check on both manager node and worker node:

```
curl http://192.168.0.13:8000
curl http://192.168.0.10:8000
```


## Docker deploy

[docker deploy](https://docs.docker.com/v17.12/edge/engine/reference/commandline/deploy/) is used to deploy a complete application stack to the swarm, which accepts the stack application in [compose file](https://docs.docker.com/compose/compose-file/), docker depoy is in experimental, which can be trigger in `/etc/docker/daemon.json`, [check to enable experimental features](https://docs.docker.com/v17.12/engine/reference/commandline/dockerd/#daemon-configuration-file)



[a sample from jianshu](https://www.jianshu.com/p/1db6f0150fdb) `docker-compose.yml`:

```
version: "3"

services:
  nginx:
    image: nginx:alpine
    ports:
      - 80:80
    deploy:
      mode: replicated
      replicas: 4

  visualizer:
    image: dockersamples/visualizer
    ports:
      - "9001:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      replicas: 1
      placement:
        constraints: [node.role == manager]

  portainer:
    image: portainer/portainer
    ports:
      - "9000:9000"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      replicas: 1
      placement:
        constraints: [node.role == manager]

```

a few commands to look into swarm services: 

```
docker stack deploy -c docker-compose.yml   stack-demo 
docker stack services  stack-demo 
docker service inspect --pretty stack-demo   # inspect service in the swarm
docker service ps <service-id>  # check which nodes are running the service
docker ps #on the special node where the task is running, to see details about the container

```

## summary

at this moment, it's not possible to use v3 compose.yml to support `runtime=nvidia`, so using v3 compose.yml to depoly a gpu-based service in swarm is blocked. the nature swarm way maybe the right solution. 


## refer 

* [run as an insecure registry](https://github.com/docker/docker.github.io/blob/master/registry/insecure.md)

* [https configure for docker registry in LAN](https://www.cnblogs.com/sparkdev/p/6890995.html)

* [a docker proxy for your LAN](https://asperti.com/en/docker-proxy-for-lan)

* [alex: deploy compose(v3) to swarm](https://github.com/alexei-led/swarm-mac/blob/master/init_swarm.sh)

* [monitor docker swarm](https://sysdig.com/blog/monitor-docker-swarm/)

* [docker swarm visulizer](https://github.com/dockersamples/docker-swarm-visualizer)

* [swarm mode with docker service](https://proxy.dockerflow.com/swarm-mode-auto/)

* [inspect a service on the swarm](https://docs.docker.com/v17.09/engine/swarm/swarm-tutorial/inspect-service/)

* [voting example](https://github.com/dockersamples/example-voting-app#linux-containers)

* [enable compose for nvidia-docker](https://yudanta.github.io/posts/nvidia-docker-and-docker-compose-enabled/)

* [nvidia-docker-compose](https://libraries.io/pypi/nvidia-docker-compose)

* [compose issue: to support nvidia under Docker compose](https://github.com/docker/compose/issues/6691)

* [potential solution for composev3 with runtime](https://github.com/docker/app/issues/241)

* [swarmkit: generic_resources](https://github.com/docker/swarmkit/blob/master/design/generic_resources.md)



