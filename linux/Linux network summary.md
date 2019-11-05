


## Linux network commands 


### ip
[ip](https://www.computerhope.com/unix/ip.htm) command is used to edit and display the configuration of network interfaces, routing, and tunnels. On many Linux systems, it replaces the deprecated ifconfig command.

```script 
ip link  del docker0   # delete a virtual network interface 
ip addr add 192.168.0.1  dev eth1  #assign IP to a specific interface(eht1)
ip addr show #check network interface 
ip addr del 192.168.0.1 dev eth1 
ip link set eth1 up/down
ip route [show] 
ip route add 192.168.0.1 via 10.10.20.0 dev eth0  #add static route 192.168.0.1
ip route del 192.168.0.1  #remove static route
ip route add default via 192.168.0.1 # add default gw
```

### netstate
[netstate](https://www.ibm.com/support/knowledgecenter/en/ssw_aix_72/n_commands/netstat.html) used to display active sockets/ports for each protocol (tcp/ip)

```script 
    netstat -lat 
    netstat -us
```

### nmcli 
[nmcli](https://developer.gnome.org/NetworkManager/stable/nmcli.html) is a Gnome command tool to control NetworkManager and report network status: 

```script 
nmcli  device status 
nmcli connection show =
```

### route
[route](http://www.softpanorama.org/Net/Netutils/route_in_linux.shtml)


```script
route  ==>  ip route (modern version) ##print router 
route add -net sample-net gw 192.168.0.1 
route del -net link-local netmask  255.255.0.0  #delete a virtual network interface 
ip route flush  # flashing routing table
```

### tracepath 
[tracepath](https://www.linux.org/docs/man8/tracepath.html) is used to traces path to a network host discovering MTU along this path. a modern version is `traceroute`.

```
tracepath 192.168.0.1 
``` 

### networking service 
```
systemctl restart networking 
/etc/init.d/networking restart 
# or
service NetworkManager stop
```


## network interface 

location at `/etc/network/interfaces` 

`eno1` is onboard Ethernet(wired) adapter. if machines has already `eth1` in its config file, for the second adapter, it will use `eno1` rather than using `eth2`.

[ifconfig](https://www.ibm.com/support/knowledgecenter/ssw_aix_71/i_commands/ifconfig.html) is used to set up network interfaces such as Loopback, Ethernet network interface: a software interface to networking hardware, e.g.  physical or virtual. physical interface, such as `eth0`, namely Ethernet network card. virtual interface such as `Loopback`, `bridges`, `VLANs` e.t.c. 


```
ifconfig -a
ifconfig eth0  #check specific network interface
ifconfig eth0 192.168.0.1 #assign static IP address to network interface
ifconfig eth0 netmask 255.255.0.0 #assign netmask 

ifconfig docker0 down/up 

```

replaced by `ip` command later.


### why enp4s0f2 instead of eth0

[change back to eth0](https://www.itzgeek.com/how-tos/mini-howtos/change-default-network-name-ens33-to-old-eth0-on-ubuntu-16-04.html)

```shell

lspci | grep -i "net"

dmesg | grep -i eth0

ip a 

sudo vi /etc/default/grub
	GRUB_CMDLINELINUX="net.ifnames=0 biosdevname=0"
update-grub

# update  /etc/network/interfaces 

auto eth0
iface eth0  inet static 

sudo reboot
 
```

### Unknown interface enp4s0f2

due TO `/etc/network/interfaces` has `auto enp4s0f2` line, which always create this network interface , when restart the networking service.


### ping hostname with docker0

usually there may be have multi network interfaces(eth0, docker0, bridge..) on a remote host, when ping this remote host with exisiting docker network (`docker0`), by default will talk to the docker0, which may not the desired one.



## build LAN cluster with office PCs

* setup PC IPs

```script 

master node: 
IP Address:  192.168.0.1 
netmask: 24
Gateway: null
DNS serer:  10.3.101.101 


worker node:

IP address:  192.168.0.12
netmask: 24
Gateway: 192.168.0.1
DNS: 10.255.18.3

``` 

* `ufw disable` 

*  update `/etc/hosts` file:  

```
    192.168.0.1 master
    192.168.0.12 worker 
``` 
if need to update the default hostname to `worker`, can modify `/etc/hostname` file, and reboot.

* ping test :

```script 

ping -c 3 master 
ping -c 3 worker 

``` 

*  set ssh access(optionally)

```script 

sudo apt-get install openssh-server 
ssh-keygen -t rsa 
# use custmized key
cp rsa_pub.key authorized_key

``` 



## refer

[Ubuntu add static route](https://www.cyberciti.biz/faq/ubuntu-linux-add-static-routing/)
[10 useful IP commands](https://www.tecmint.com/ip-command-examples/)

