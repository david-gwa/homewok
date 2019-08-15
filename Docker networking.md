
 

## at first

for our framework, the host Docker (manager) container is running at master node, and there are a bunch of Docker (worker) containers running on worker nodes, one by one. 

requirements for the manager container: 

1) when the manager click `start`, all worker containers start to do its job, which may need to fetch from the manager node. 

2) if there is any worker goes wrong, the manager node should be known

3) the worker may send a result/report to manager when the job is done


requiremnets for the worker container: 

1) the lg-sim works as a server, and there should be a Python client running and getting data from the server, the Python client is hosted in the same host or from remote control.



get into the Docker container:

        docker exec -it  

        docker run -it 



### Docker network drivers
[refer](https://docs.docker.com/network/)

* bridge:  the default network driver, only in standalone containers; best when have multiple containers to communicate on the same host machine.

* host: for standalone containers, the Docker host use the host machine's networking directly; best when need no isolated from the host machine.

* overlay: connect multi Docker containers, enable swarm services to communicate with each other, no OS-level routing; best when need containers running on different host machines to communicate.

* none: disable all networking

### overlay networking 
[tutorial refer](https://docs.docker.com/network/network-tutorial-overlay/)
[user refer](https://docs.docker.com/network/overlay/)


```shell

#start a swarm on (manager) node

docker swarm init --advertise-addr=192.168.0.1 

#join swarm on (worker) node

docker swarm join --token  manager-generated-token  --advertise-addr 192.168.0.12  192.168.0.1:2377

# on manager node

docker network create -d overlay --attacheable ppss-overlay
docker service create --name ppss-demo --publish 80  --replicas=5 --network ppss-overlay ppss-demo

## inspect service
docker service inspect ppss-demo
## remove service 
docker service rm ppss-demo
## remove network
docker network rm ppss-demo
	
```


## Docker communication

[Docker communicate via hostname](https://stackoverflow.com/questions/30545023/how-to-communicate-between-docker-containers-via-hostname)


[blowb project](http://docs.blowb.org/index.html)


[ownCLoud](https://doc.owncloud.org/server/10.2/)

[huashengke](https://www.oray.com/)


### Docker network

```shell
	
docker network create ppss

docker run --net=ppss  lg-runner-worker  

docker network connect ppss  lg-runner-master 

docker exec -it lg-runner-master ping lg-runner-worker
```

###  DNS


## Docker images distribute

### upload to Docker HUB (public)

### build private repository(private) 

 not only Docker images, if we have private repository, we can also manage the scenes
 
[refer](http://littlebigextra.com/installing-docker-images-private-repositories-docker-swarm/) 

### local save/export 

save images to tar and distribute through ssh

```shell
#on master node 
sudo docker save -o  /path/to/save/file  lg-runner[image]  | gzip  

scp lg-runner.tar.gz  user@tsuipc:~

#on worker node 
unzip -xfvz lg-runner.tar.gz  | docker load 

```

actually, if the docker swarm networking is created, should be OK to transfer through the swarm-networking. TODO.



[refer](https://blog.giantswarm.io/moving-docker-container-images-around/)




