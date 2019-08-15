

## Linux Network


[nmcli & setup network](https://blog.csdn.net/m0_38044196/article/details/72899929)


### check network interface card 

```shell 

/sys/class/net:

lrwxrwxrwx 1 root root 0 Jul  2 21:21 docker0 -> ../../devices/virtual/net/docker0
lrwxrwxrwx 1 root root 0 Jul  2 21:20 eth0 -> ../../devices/pci0000:00/0000:00:1c.4/0000:02:00.0/0000:03:03.0/0000:04:00.2/net/eth0
lrwxrwxrwx 1 root root 0 Jul  2 21:20 lo -> ../../devices/virtual/net/lo

```


### nmcli 

```shell
 nmcli con show

 nmcli dev status 

 sudo service network-manager restart 
```



### network interfaces config

location: `/etc/network/interfaces`


### ifconfig 

used to set up network interfaces such as Loopback, Ethernet

network interface: a software interface to networking hardware, e.g.  physical or virtual.

physical interface, such as `eth0`, namely Ethernet network card. virtual interface such as `Loopback`, `bridges`, `VLANs` e.t.c

  
the output of `ifconfig` is all network interfaces on current system


### why  enp4s0f2 instead of eth0 

[anwer](https://www.ringingliberty.com/2019/06/05/change-multiple-interface-ips-with-networkd-on-coreos/)

/etc/systemd/network/enp4s0f1.network


/etc/udev/rules.d/70-persistent-net.rules

[change back to eth0](https://www.itzgeek.com/how-tos/mini-howtos/change-default-network-name-ens33-to-old-eth0-on-ubuntu-16-04.html)

```shell

lspci | grep -i "net"

dmesg | grep -i eth0

ip a 

sudo vi /etc/default/grub
	GRUB_CMDLINELINUX="net.ifnames=0 biosdevname=0"
update-grub

// update  /etc/network/interfaces 

auto eth0
iface eth0  inet static 

sudo reboot
 
```


### set eth0 with two ip address



### ping network interface to docker0

on  tsuipc:

ping ubuntu -->  it actually talk to Docker0 (virtual), rather than (ppss-master)



## Docker network




## port & port mapping 

define ports in Docker,



## login to container

```shell 
docker exec -it container-name  /bin/bash 

```


## create a new image 

[refer](https://www.mirantis.com/blog/how-do-i-create-a-new-docker-image-for-my-application/0)

 imagename format:  [username]/[imagename]:[tags]


 ```shell

  docker commit -m " "  -a "author " [containername] [imagename]

  docker push [imagename]
 
  docker images 

  #for test
 
  docker stop  existing-image-container
 
  docker rm  existing-image-container 

  docker rmi existing-image 

  docker images 

  docker run -dP  [imagename]

  docker ps 

```
  

  
## from jjin2 to davidzjj

 [refer2](https://www.techrepublic.com/article/how-to-commit-changes-to-a-docker-image/)

 terminal1: ./run_lg_docker.sh

 terminal2: 

   docker ps # get container-ID
   docker exec -it container-ID  /bin/bash 
   
 apt list  --installed  
 apt-get --purge remove cuda*
 apt-get --purge remove  libcudnn*

 pip freeze 
 pip uninstall tensorflow-gpu 
 pip uninstall  Keras-*


  exit
  docker ps   #check the container-ID 

  docker commit -m " "  -a ""  container-ID   davidzjj/lg-sim:vx 

  

### from docker images to Dockfile

connecting issue: 

/usr/lib/ruby/gems/2.2.0/gems/docker-api-1.24.1/lib/docker/connection.rb:42:in `rescue in request': 400 Bad Request: malformed Host header (Docker::Error::ClientError)
	from /usr/lib/ruby/gems/2.2.0/gems/docker-api-1.24.1/lib/docker/connection.rb:38:in `request'
	from /usr/lib/ruby/gems/2.2.0/gems/docker-api-1.24.1/lib/docker/connection.rb:65:in `block (2 levels) in <class:Connection>'
	from /usr/lib/ruby/gems/2.2.0/gems/docker-api-1.24.1/lib/docker/image.rb:172:in `all'
	from /usr/src/app/dockerfile-from-image.rb:32:in `<main>'





[build image](https://www.howtoforge.com/tutorial/how-to-create-docker-images-with-dockerfile/)


 





 





