## backgroud 

our application so far includes the following three services:

* simulator

* pythonAPI

* redisJQ

**docker swarm network** has the following three kind of networks, of course `bridge` to host network.

* overlay network, services in the same overlay network, can communicate to each other 

* routing network, the service requested can be hosted in any of the running nodes, further as load balancer.

* host network 

usually,  [multi-container apps can be deployed with docker-compose.yml](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/multi-container-applications-docker-compose), check [docker compse](https://docs.docker.com/compose/compose-file/) for more details.


## DNS service discovery 

the following is an example from ([overlay networking and service discovery](https://github.com/docker/labs/blob/master/networking/A3-overlay-networking.md):


my test env includes 2 nodes, with host IP as following. when running docker services, it will generate a responding virtual IP, while which is dynamic assgined. 

| hostname | virtualIP | hostIP  | 
|--|--|--|
| node1 | 10.0.0.4 | xx.20.181.132 | 
| node2 | 10.0.0.2 | xx.20.180.212 | 


a common issue when try first to use overlay network in swarm, e.g. ping the other service doesn't work, check `/etc/resolv.conf` file: 

```sh 
# cat /etc/resolv.conf 
nameserver 8.8.8.8
nameserver 8.8.4.4
``` 

the default `dns=8.8.8.8` can't ping either hostIP or any docker0 IP. the reason can find [#moby/#23910](https://github.com/moby/moby/issues/23910): When spinning up a container, Docker will by default check for a DNS server defined in /etc/resolv.conf in the host OS, and if it doesn't find one, or finds only 127.0.0.1, will opt to use Google's public DNS server 8.8.8.8. 

one solution mentioned:

* cat /etc/docker/daemon.json 

```xml
{

		"dns": ["172.17.0.1", "your.dns.server.ip", "8.8.8.8"]
}

```

*  add a file `/etc/NetworkManager/dnsmasq.d/docker-bridge.conf`

```sh
listen-address=172.17.0.1
```

so basically, the default DNS setting only listens to DNS requests from 127.0.0.1 (ie, your computer). by adding `listen-address=172.17.0.1`, it tells it to listen to the docker bridge also. very importantly, **Docker DNS server is used only for the user created networks**, so need create a new docker network. if use the default `ingress` overlay network, the dns setup above still doesn't work.

another solution is using **host network**, mentioned [using host DNS in docker container with Ubuntu](https://l-lin.github.io/post/2018/2018-09-03-docker_ubuntu_18_dns/) 


#### test virtualIP network

* create a new docker network

```sh
 docker network create -d overlay l3
```

why here need a new network ?  due to **Docker DNS server(172.17.0.1) is used only for the user created networks**

* start the service with the created network: 

```sh
docker service create --name lg --replicas 2 --network l3 20.20.180.212:5000/lg
``` 

* check vip on both nodes

```sh
 docker network inspect l3 
```

check vip by the line `IPv4Address`:

```
node1 vip : `10.0.1.5/24`
node2 vip: `10.0.1.6/24` 
```

* go to the running container 

```sh
docker exec -it 788e667ea9cb  /bin/bash 
apt-get update && apt-get install iputils-ping
ping 10.0.1.5
ping 10.0.1.6
```

* now ping service-name directly 

```sh 
ping lg 
PING lg (10.0.1.2) 56(84) bytes of data.
```

* inspect service 

```sh 
docker service inspect lg 
            "VirtualIPs": [
                {
                    "Addr": "10.0.1.2/24"
                }
            ]
```


* ping host IP from contianer vip

as far as we add both `host dns` and `docker0 dns` to the dns option in `/etc/docker/daemon.json`, the container vip can ping host IP.


#### assign ENV variable from script 


* get services vip 

[get vip list](https://serverfault.com/questions/925267/how-do-i-list-docker-vip-addresses)

```sh
vip=`sudo docker service inspect --format '{{.Endpoint.VirtualIPs}}'  lgsvl | awk '{print substr($2, 1, length($2)-5)}'`
echo $vip
```


* create docker service with runtime env


```sh
ping -c 1 lg  | awk 'NR==1 {print $2}' 
``` 


## redis service 

there is a common error: `redis.exceptions.ConnectionError: Error 111 connecting to 10.20.181.132:6379. Connection refused.` , which basically means the system can't connect to redis server, due to by default redis [only allow localhost](https://www.cnblogs.com/likwo/p/5903377.html) to access. so we need configure non-localhost IP to access redis db. 


* check redis-server running status 

```sh
ps aux | grep redis-server
netstat -tunple | grep 6379
redis-cli info 

```

* shutdown redis-server

```sh
sudo kill -9 $pid
```

#### redis-server & redis-cli 

**redis-server & redis-cli**

`redis-server` start redis server with a default config file at `/etc/redis/redis.config`

a few item in the configure file need take care:

* bind, check [here](https://stackoverflow.com/questions/16120287/redis-bind-to-more-than-one-ip)

the default setting is to `bind 127.0.0.1`,which means redis db is stored and only can be access through `localhost`.  for our case, to allow hostIP(10.20.181.132), or even any IP to access, need :

```xml
bind 0.0.0.0
```

* redislog, default place at `/var/log/redis/redis-server.log` 


*  requirepass, for [security issues](https://blog.csdn.net/qq_40460909/article/details/84838245), please consider this item

* login client with hostIP

```sh
redis-cli -h 10.20.181.132
```

* [basic operation of redis-cli](https://www.tutorialspoint.com/redis/redis_lists.htm)

log in redis-cli first, then run the following: 

```sh
LPUSH your_list_name item1 
LPUSH your_list_name item2 
LLEN your_list_name
EXISTS your_list_name
```

#### redis service in docker 

the following is an example from [create a redis service](https://docker-doc.readthedocs.io/zh_CN/stable/examples/running_redis_service.html)

* connect to the redis container directly

```sh
docker run -it redis-image /usr/bin/redis-server /etc/redis/myconfig.conf 
```

in this way, `redis service` will use its docker VIP, which can be checked from:

```sh
docker ps 
docker inspect <container_id>
```

which will give somehing like:

```xml
                "bridge": {
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
```

then the redis-server can connect by:

```sh
redis-cli -h 172.17.0.2
```

* connect to the host os 

```sh
docker run -it -p 6379 redis-image /usr/bin/redis-server /etc/redis/myconfig.conf 
```

**the redis container has exported 6379, which may map to another port on host os**, check:

```sh
docker ps 
docker port <container_id> 6379  #gives the <exernal_port> on host
rdis-cli -h 10.20.181.132 -p <external_port>
```

* run redis service with host network

```sh
docker run -it --network=host redis-image /usr/bin/redis-server /etc/redis/myconfig.conf 
```

in this way, there is no bridge network, or docker VIP. the host IP and port is directly used. so the following works

```sh
redis-cli -h 10.20.181.132 -p 6379
```


A good way now, is to map host redis_port to container redis_port, and use the second way to access redis.

```sh
docker run -it -p 6379:6379 redisjq /bin/bash 

```

tips, need to confirm `6379` port at host machine is free.


#### share volumes among multi volumes

the problem is `redisjq service` download all scenarios scripts in its own docker container, and only store the scenario name in `redis db`. when `redis_worker` access the db, there is no real python scripts. so need to share this `job-queue` to all `redis_worker`s


[mount volume](https://docs.docker.com/storage/volumes/)

```sh
docker run -it -p 6379:6379 --mount source=jq-vol,target=/job_queue redisjq /bin/bash
```

#### start pythonapi to access the shared volume

```sh
docker run -it --mount source=jq-vol,target=/pythonAPI/job_queue  redispythonapi  /bin/bash
```
 

## multi-services test

#### run all services in single docker mode

```sh
docker run -it -p 6379:6379 --mount source=jq-vol,target=/job_queue redisjq /bin/bash 
docker run xx.xx.xx.xxx:5000/lg
docker run -it --mount source=jq-vol,target=/pythonAPI/job_queue xx.xx.xx.xxx:5000/redispythonapi  /bin/bash
```


* check docker-IP of `lg` :

```sh
docker sh 
docker container inspect <lg> #get its IP-address
```

* update `SIMULATOR_HOST` for `redispythonapi` 

```sh
docker exec -it <redispythonapi> /bin/bash
export SIMULATOR_HOST=lg_ip_address #from the step above
./redis_worker.sh  #where all python scenarios are running in queue
```

here we can check the lg container's IP is `172.17.0.3` and redispythonapi's IP is `172.17.0.4`, then update `start_redis_worker.sh` with `SIMULATOR_HOST=172.17.0.3`

* get the container IP

```sh
docker container ls  | grep -w xx.xx.xx.xxx:5000/lg | awk '{print $1}' 
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'  $(docker container ls  | grep -w xx.xx.xx.xxx:5000/lg | awk '{print $1}' )
```

## assign a special IP to service in swarm

docker network create support [subnet](https://docs.docker.com/engine/reference/commandline/network_create/), which only ip-addressing function, namely we can use custom-defined virtual IP for our services. a sample: 

```sh
docker network create -d overlay \
  --subnet=192.168.10.0/25 \
  --subnet=192.168.20.0/25 \
  --gateway=192.168.10.100 \
  --gateway=192.168.20.100 \
  --aux-address="my-router=192.168.10.5" --aux-address="my-switch=192.168.10.6" \
  --aux-address="my-printer=192.168.20.5" --aux-address="my-nas=192.168.20.6" \
  my-multihost-network
``` 

we can run our application as:

```sh
docker network create --driver=overlay --subnet=192.168.10.0/28  lgsvl-net
docker service create --name lgsvl --replicas 2 --network lgsvl-net --host "host:192.168.10.2"  xx.xx.xx.xxx:5000/lgsvl
docker service create --name redis --replicas 1 --network lgsvl-net  -p 6379:6379 --mount source=jq-vol,target=/job_queue  --constraint 'node.hostname==ubuntu' xx.xx.xx.xxx:5000/redisjq
docker service create --name pythonapi --replicas 1 --network lgsvl-net --mount source=jq-vol,target=/pythonAPI/job_queue  xx.xx.xx.xxx:5000/redispythonapi
```

[understand subnet mask](https://www.cnblogs.com/milantgh/p/4075912.html). IP address include `master IP` and `subnet mask`, we choose `28` here, basically generate about `2^(32-28)-2= 14` avaiable IP address in the subnet. but in a swarm env, subnet IPs are consuming more as the nodes or replicas of service increase.

taking an example, with 2-nodes and 2-replicas of service, **5 subnet IPs are occupied, rather than 2**

run `docker network inspect lgsvl-net` on both nodes:

* on node1 gives:

```xml
lg.1 IPV4Address: 192.168.10.11/28
lgssvl-net-endpoint: 192.168.10.6/28
```

* on node2 gives:

```xml
lg.2 IPV4Address: 192.168.10.4/28
lgssvl-net-endpoint: 192.168.10.3/28
``` 

* `docker service inspect lg` gives:

```xml
VirualIPs: 192.168.10.2/28
```

clearly 5 IP address are occupied. and the IP for each internal service is random picked, there is no gurantee `service` will always get the first avaiable IP. 


#### docker serivce with --ip

**only docker run --ip** works, there is no similar `--ip` option in `docker service create`. but a lot case require this feature: [how to publish a service port to a specific IP address](https://success.docker.com/article/how-do-i-publish-a-service-port-to-a-specific-ip-address),  when publishing a port using `--publish`, the port is published to `0.0.0.0` instead of a specific interface's assigned IP. and there is no way to assign an fixed IP to a service in swarm. 

a few disscussion in [moby/#26696](https://github.com/moby/moby/issues/26696), [add more options to `service create](https://github.com/moby/moby/issues/25303), [a possible solution](https://github.com/moby/moby/issues/24170#issuecomment-300771012), [Static/Reserved IP addresses for swarm services](https://github.com/moby/moby/issues/24170)

mostly depend on the issues like "ip address is not known in advance, since docker service launched in swarm mode will end up on multiple docker servers". there should not be applicable to docker swarm setup, since if one decides to go with docker swarm service, has to accept that service will run on multiple hosts with different ip addresses. I.e. trying to attach service / service instance to specific IP address somewhat contradicting with docker swarm service concept. 


[docker service create](https://docs.docker.com/engine/reference/commandline/service_create/) does have options `--host host:ip-address` and `--hostname` and similar in [docker service update](https://docs.docker.com/engine/reference/commandline/service_update/)  support `host-add` and `host-rm`.

```sh
$ docker service create --name redis --host "redishost:192.168.10.2" --hostname myredis redis:3.0.6
``` 

then exec into the running container, we can check out `192.168.10.2 redishost` is one line in `/etc/hosts` and `myredis` is in `/etc/hostname`

but remember, the DNS for this hostIP(192.168.10.2) should be first configured in the docker engine DNS list. if not, even the hostIP is in the arrange of the subnet, it is unreachable from the containers.

[another explain](https://www.freecodecamp.org/news/docker-nginx-letsencrypt-easy-secure-reverse-proxy-40165ba3aee2/): by default docker containers are put on their own network. This means that you won’t be able to access your container by it’s hostname, if you’re sitting on your laptop on your host network. It is only the containers that are able to access each other through their hostname.


#### dnsrr vs vip 

```sh
--endpoint-mode dnsrr
```


`dnsrr` mode, namely DNS round Robin mode, when query Docker's internal DNS server to get the IP address of the service, it will return IP address of every node running the service.

`vip` mode, return the IP address of only one of the running cntainers. 

When you submit a DNS query for a service name to the Swarm DNS service, it will return one, or all, the IP addresses of the related containers, depending on the endpoint-mode.

[dnsrr vs vip](https://stackoverflow.com/questions/42875572/how-to-load-balance-websocket-apps-in-docker-swarm): Swarm defaults to use a virtual ip (endpoint-mode vip). So each service gets its own IP address, and the swarm load balancer assigns the request as it sees fit; to prevent a service from having an IP address, you can run `docker service update your_app --endpoint-mode dnsrr`, which will allow an internal load balancer to `run a DNS query against a service name`, to discover each task/container's IP for a given service

in our case, we want to assign a speical IP to the service in swarm. **why?** because our app has websocket server/client communicataion, which is IP address based. we can' assign `service name` for WS server/client.

check another issue: [dockerlize a websocket server](https://stackoverflow.com/questions/54101508/how-do-you-dockerize-a-websocket-server)



## global mode to run swarm

when deploying service with global mode, namely each node will only run one replicas of the service. the benefit of `global mode` is we can always find the node IP, no matter the IP address is in host network or user-defined overlay network/subnetwork. 

#### get service's IP in global mode 

[get listened port](https://www.cyberciti.biz/faq/unix-linux-check-if-port-is-in-use-command/)

```sh
root@c7279faebefa:/lgsvl# netstat -tulpn | grep LISTEN
tcp        0      0 127.0.0.11:33263        0.0.0.0:*               LISTEN      -               
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      7/lgsvl_Core.x86_64
tcp        0      0 0.0.0.0:8181            0.0.0.0:*               LISTEN      7/lgsvl_Core.x86_64

```

both `8080` and `8181` is listening after `lgsvl` service started. on the `lgsvl` side, we can modify it to listen on all address with `8181` port. then the following [python script](https://www.jb51.net/article/173931.htm) to find node's IP:

```py
import socket
 
def get_host_ip():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
  finally:
    s.close()
 
  return ip
```

in this way, no need to pre-define the `SIMULATOR_HOST` env variable at first. the pythonAPI only need to find out its own IP and detect if `8181` is listening on in runtime.

#### container vs service 

[difference between service and container](https://stackoverflow.com/questions/43408493/what-is-the-difference-between-docker-service-and-docker-container):

* `docker run` is used to create a standalone container

* `docker service` is the one run in a distributed env. when create a service, you specify which container image to use and which commands to execue inside the running containers. 

There is only one command(no matter the format is `CMD` `ENTRYPOINT` or `command in docker-compose`) that docker will run to start your container, and when that command exits, the container exits. in swarm service mode, with default restart option(any), the container run and exit and restart again with a different containeID. check [dockerfile, docker-compose and swarm mode lifecycle](https://stackoverflow.com/questions/56328330/dockerfile-docker-compose-and-swarm-mode-lifecycle) for details. 


#### [docker container restart policy](https://rollout.io/blog/ensuring-containers-are-always-running-with-dockers-restart-policy/):

[docker official doc: start containers automatically](https://docs.docker.com/config/containers/start-containers-automatically/)

* no, simply doesn't restart under any circumstance 

* on-failure, to restart if the exit code has error. user can specify a maximum number of times Docker will automatically restart the container; the container will not restart when app exit with a successful exit code. 

* unless-stopped, only stop when Docker is stopped. so most time, this policy work exactly like `always`, one exception, when a container is stopped and the server is reboot or the DOcker serivce is restarted, the container won't restart itself. if the container was running before the reboot, the container would be restarted once the system restarted.

* always, tells Docker to restart the container under any circumstance. and the service will restart even with reboot. any other policy can't restart when system reboot.


similar restart policy can be found in :

* [docker-compose restart policy](https://docs.docker.com/compose/compose-file/#restart_policy)


* [docker service create restat-condition](https://docs.docker.com/engine/reference/commandline/service_create/)


#### keep redisJQ alive in python script 

by default setup, `redis server` is keep restarting and running, which make the `pythonapi` service always report: ` redis.exceptions.ConnectionError: Error 111 connecting to xx.xxx.xxx:6379. Connection refused.`

so we can keep redisJQ alive in python script level by simply a `while loop`.

for test purpose, we also make pythonAPI restart policy as none, so the service won't automatically run even with empty jobQueue.


the final test script can run in the following:

```sh
docker service create --name lgsvl --network lgsvl-net --mode global xx.xx.xx.xxx:5000/lgsvl
docker service create --name redis -p 6379:6379 --network lgsvl-net --mount source=jq-vol,target=/job_queue  --constraint 'node.hostname==ubuntu' xx.xx.xx.xxx:5000/redisjq 
docker service create --name pythonapi --network lgsvl-net --mode global --mount source=jq-vol,target=/pythonAPI/job_queue --restart-condition none xx.xx.xx.xxx:5000/pythonapi
```


#### use python variable in os.system

[sample](https://stackoverflow.com/questions/27128851/how-to-use-python-variable-in-os-system)

```python
os.system("ls -lt %s"%your_py_variable)
```



## proxy in docker swarm


[HAProxy](https://www.haproxy.com/blog/haproxy-on-docker-swarm-load-balancing-and-dns-service-discovery/)

Routing external traffic into the cluster, load balancing across replicas, and DNS service discovery are a few capabilities that require finesse. but proxy can't either assign a special IP to a special service, neither can expose the service with a fixed IP, so in our case, no helpful.











