### why Docker machine 

Docker Machine allow to batch install and configure Docker host env, no need to individually install each Docker on each host.


### instal Docker machine 

* on master host:

```shell
curl -L https://github.com/docker/machine/releases/download/v0.9.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&

  chmod +x /tmp/docker-machine &&

  sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
```

addtionaly, install `bash completion script` 


tips: 

```shell
ssh-copy-id  [-i identify_file] [user@]machine 
```

by default, the `identify_file` is  `~/.ssh/id_rsa.ub`.  `ssh-copy-id` will copy ssh-pub-key at local host to the same user at remote host 

(base) ubuntu@ubuntu:~$ docker-machine create --driver generic  --generic-ip-address=192.168.0.1 --generic-ssh-key ~/.ssh/ps_master_id_rsa --generic-ssh-user ubuntu  docker-master 



Error creating machine: Error running provisioning: ssh command error:
command : sudo hostname docker-master && echo "docker-master" | sudo tee /etc/hostname
err     : exit status 1
output  : sudo: no tty present and no askpass program specified

by default, docker-machine requires  `root` privilige, if not, there will be the error as above. 





#### docker machine ssh

 generate new ssh key

```shell

 ssh-keygen -t rsa 

 ssh-copy-id  -i id_rsa 192.168.0.1   ## check  authorized_keys file, there should be a new one added

```



##### user run sudo without passwd


[refer](https://www.tecmint.com/run-sudo-command-without-password-linux/)

[ubuntu host](https://help.ubuntu.com/community/Sudoers)


at /etc/sudoers adding:

` user  ALL=(ALL) NOPASSWD: ALL `


rerun:

```shell
(base) ubuntu@ubuntu:~$ docker-machine create --driver generic  --generic-ip-address=192.168.0.1 --generic-ssh-key ~/.ssh/ps_master_id_rsa --generic-ssh-user ubuntu  docker-master   
Running pre-create checks...
Creating machine...
(docker-master) Importing SSH key...
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with ubuntu(systemd)...
Installing Docker...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...
Checking connection to Docker...
Docker is up and running!
To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: docker-machine env docker-master


```


### use Docker Machine to run Docker containers 

[doc](https://docs.docker.com/machine/get-started/)




## swarm

(base) ubuntu@docker-master:~/zj/docker$ sudo docker swarm join-token manager 

docker swarm join --token SWMTKN-1-5z5n3r6q93ymjxx2p3dxqtd0w5l775513ieik6ll3q9ncm3rbh-b4wq0xy5ks5yrq81krpiwk4lt 192.168.0.1:2377


## service 

a service is a long-running Docker container that can be deployed to any node worker. 

 
```shell 

docker service create --name web_server  httpd

docker service ls

docker service scale  web_server=3    ##how to scale 
```

[build your own service](https://www.jianshu.com/p/a3a83f236c85)




how to start a lg-runner service :


sudo docker service create --replicas 3 --name lg-sim-runner lg-runner sudo nvidia-docker run -it -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix  lg-runner /bin/bash 


* how swarm find out the service ? 

if not external communication and in `Running` status, will be considered as `Preparing`

if mapped with port ID, will be considered as `Running`


#### how service work

[refer](https://docs.docker.com/v17.12/engine/swarm/how-swarm-mode-works/services/)

in a service, to specify which container image to use and which commands to execute


[how service work](https://semaphoreci.com/community/tutorials/consuming-services-in-a-docker-swarm-mode-cluster)




### depoly service to swarm

define the image name and tag the service containers should run

whether the service should start automatically

the created service is scheduled on an avialable node, 

you can specify a command that the service's container should run, by adding the command after image name



#### configure service runtime environment 

  `--env`:  environment variable


#### run nvidia-docker as service 


 
 


