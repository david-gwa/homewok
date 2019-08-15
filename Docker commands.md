
# Docker commands 

[docker base commands](https://docs.docker.com/engine/reference/commandline/docker/)

## container related commands

### docker checkpoint 
manage checkpoints 

### docker container
	list avaiable containers in localhost

### docker create 
	create a new container 

### docker export 
	export a container's filesystem as a tar archive

### docker inspect 
	return low-level info on Docker objects

### docker kill

### docker load 

### docker logs 
	output container info to stdout

### docker run
	run a command in a new container 
-e/--env ,  set env variables 
-v/--volume,  bind mount a volume 
--net,  connect a container to a network 
-p/-publish, publish a container's ports to the host 
-P/-publish-all,  publish all exposed ports to random ports
--name,  assigne a name to the container 
--ip,  IPV4 address
--hostname/-h,   container host name 
--rm, automatically remove the container when it exists


### docker start
	start stopped containers 

### docker stop
	stop running containers

### docker ps 
	check running containers info

### docker rm  
	remove containers 


## image related commands:

### docker build
build an image from Dockfile


### docker images 
	manage images 

### docker pull

### docker push

### docker save 
	save images to a tar

### docker search
	search Docker Hub for images 



## docker with GUI

[glxinfo docker](https://github.com/coreyryanhanson/dockerfiles/tree/master/glxgears)
[jess libreoffice](https://github.com/jessfraz/dockerfiles/tree/master/libreoffice)
[Docker run GUI](https://www.csdn.net/article/2015-07-30/2825340)


## docker GUI on ssh remote


## stop and clean docker containers
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)



##

standard_init_linux.go:211: exec user process caused "permission denied"

[docker container exist immediately](https://stackoverflow.com/questions/28212380/why-docker-container-exits-immediately)


(base) ubuntu@ubuntu:~/zj/lg-sim$ sudo docker-compose  up build 




