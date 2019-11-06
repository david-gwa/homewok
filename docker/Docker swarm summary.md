

### Docker micro services 

[key concepts in Docker](https://docs.docker.com/v17.09/engine/swarm/key-concepts/#services-and-tasks)

when deploy an application(lg-sim) to swarm cluster as a service, which is defined in a/the manager node, the manager node will dispatch units of work as taskes to worker nodes.

when create a service, you specify which container image to use and which commands to execute inside runing containers. In the `replicated services`, the swarm manager distributes a specific number of replica tasks among the nodes based upon the scale you set in the desired state. For `global services`, the swarm runs one task for the service on every available node in the cluster.


![docker node](https://docs.docker.com/v17.09/engine/swarm/images/swarm-diagram.png)



#### Docker swarm CLI commands 
```script 
docker swarm init 
docker swarm join

docker service create  --name  --env --workdir --user
docker service inspect 
docker service ls 
docker service rm
docker service scale 
docker service ps
docker service update  --args

docker node inspect 
docker node update --label-add 
docker node promote/demote 
# run in worker
docker swarm leave
# run in manager
docker node rm worker-node

docker ps  #get running container ID
docker exec -it containerID /bin/bash
docker run -it
docker-compose up build/run

``` 


#### delete unused Docker network

as Docker network may confuse external when access to the local network interfaces, sometimes need to remove the docker networks.

```script 

docker network ls

docker network disconnect -f  {network} {endpoint-name}

docker network rm 

docker stop $(docker ps -a -q)

docker rm $(docker ps -a -q)

docker volume prune 

docker network prune 

```

the above scripts will delete the unused(non-active) docker network, then may still active docker related networks, which can be deleted through:

```script
sudo ip link del docker0
``` 


### access Docker service 

Docker container has its own virutal IP(172.17.0.1) and port(2347), which allowed to access in the host machine; for externaly access, need to map the hostmachine IP to docker container, by `--publish-add`. the internal communication among docker nodes are configured by `advertise_addr` and `listen-addr`.


#### through IP externaly
To publish a service’s ports externally, use the --publish <PUBLISHED-PORT>:<SERVICE-PORT> flag. When a user or process connects to a service, any worker node running a service task may respond.

taking example from [5mins series](https://www.cnblogs.com/CloudMan6/tag/Swarm/)

```script 
docker service create --name web_server --replicas=2 httpd 
docker service ps web_server 
# access service only on host machine through the Docker IP
curl 172.17.0.1 
docker service update --publish-add 8080:80 web_server
# access service externally
curl http://hostmachineIP:8080
```

#### configure websocket protocol

for lg-sim server to pythonAPI client, which is communicated through `websocket`, it's better if the service can be configured to publish through websocket.


#### publish httpd server to swarm service 

```script 
docker service create --name web_server --publish 880:80 --replicas=2  httpd 
```
the container IP is IP in network interface `docker0`(e.g. 172.17.0.1), which can be checked through `ifconfig`.  `80` is the default port used by httpd, which is mapped to the host machine `880` port. so any of the following will check correctly:


```script
curl 172.17.0.1:880
curl localhost:880
curl 192.168.0.1:880  
curl 192.168.0.13:880 #the other docker node
```

 
#### publish lg-sim into swarm service 

the previous version(2019.04) of lg-sim doesn't have a http server built-in, since 2019.7, they have `Nancy http server`, which is a great step toward dockerlize the lg-sim server.






### manage data in Docker 

`Volumes` are stored in a part of the host filesystem, which is located `/var/lib/docker/volumes`, which is actually managed by Docker, rather than by host machine.
Volumes are the preferred way to [persist data in Docker](https://docs.docker.com/v17.09/engine/admin/volumes/#more-details-about-mount-types) containers and services. some use cases of volume:

* once created, even the container stops or removed, the volume still exist.
* multiple containes can mount the same voume simultaneously; 
* when need to store data on a remote host 
* when need to backup, restore, or migrate data from one Dockr to another

#### RexRay

an even high-robost way is to separate volume manager and storge provider manager. [Rex-Ray](https://rexray.readthedocs.io/en/v0.3.3/)


```script 

docker service create --name web_s \
	--publish 8080:80 \
	--mount "type=volume, volume-driver=rexray, source=web_data, target=/usr/local/apache2/htdocs" \
	httpd

docker exec -it containerID 
ls -ld /usr/local/apahce2/htdocs
chown www-data:www-data 
## test visit
curl http://192.168.0.1:8080 
docker inspect containerID 

```

`source` reprensents the name of data volume, if null, will create new
`target` reprensents data volume will be mounted to `/usr/local/apache2/htdocs` in each container


in RexRay, data volume update, scale, failover(when any node crashed, the data volume won't lose) also be taken care.





### refer

[5mins in Docker](https://www.cnblogs.com/CloudMan6/tag/Swarm/)

[Docker swarm in and out](https://www.bookstack.cn/read/docker-swarm-guides/kai-shi-shi-yong-swarm-swarmmo-shi-duan-kou-lu-you.md)

[what is swarm advertise-addr](https://boxboat.com/2016/08/17/whats-docker-swarm-advertise-addr/)

[can ran exec in swarm](https://www.reddit.com/r/docker/comments/a5kbte/run_docker_exec_over_a_docker_swarm/)

[execute a command within docker swarm service](https://stackoverflow.com/questions/39362363/execute-a-command-within-docker-swarm-service)
























