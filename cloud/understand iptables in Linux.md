
## background 

本文是基于[iptable详解](http://www.zsythink.net/archives/1199)整理的。 理解iptables，是为了更好的理解k8s中网络。

从逻辑上讲。防火墙可以大体分为主机防火墙和网络防火墙。
主机防火墙：针对于单个主机进行防护。

网络防火墙：往往处于网络入口或边缘，针对于网络入口进行防护，服务于防火墙背后的本地局域网。

**iptables**其实不是真正的防火墙，我们可以把它理解成一个客户端代理，用户通过iptables这个代理，将用户的安全设定执行到对应的"安全框架"中，这个"安全框架"才是真正的防火墙，这个框架的名字叫**netfilter**

Netfilter是Linux操作系统核心层内部的一个数据包处理模块，它具有如下功能：

* 网络地址转换(Network Address Translate)

* 数据包内容修改

* 以及数据包过滤的防火墙功能


规则一般的定义为"如果数据包头符合这样的条件，就这样处理这个数据包". 规则分别指定了源地址、目的地址、传输协议（如TCP、UDP、ICMP）和服务类型（如HTTP、FTP和SMTP）等.  当数据包与规则匹配时，iptables就根据规则所定义的方法来处理这些数据包，如放行（accept）、拒绝（reject）和丢弃（drop）等。配置防火墙的主要工作就是添加、修改和删除这些规则。

如果我们想要防火墙能够达到"防火"的目的，则需要在内核中设置关卡，所有进出的报文都要通过这些关卡，经过检查后，符合放行条件的才能放行，符合阻拦条件的则需要被阻止，于是，就出现了input关卡和output关卡，而这些关卡在iptables中不被称为"关卡",而被称为"链"。当客户端发来的报文访问的目标地址并不是本机，而是其他服务器，当本机的内核支持IP_FORWARD时，我们可以将报文转发给其他服务器。这个时候，我们就会提到iptables中的其他"关卡"，也就是其他"链"，他们就是  "路由前"、"转发"、"路由后"，他们的英文名是

PREROUTING、FORWARD、POSTROUTING

![image](http://www.zsythink.net/wp-content/uploads/2017/02/021217_0051_2.png)


当我们定义iptables规则时，所做的操作其实类似于"增删改查"。


"关卡“/”链“ 包括：  prerouting, INPUT, OUTPUT, FORWARD, POSTROUTING

表： filter 负责过滤(iptables_filter); nat(network address translation), 网络地址转发， mangle, raw


表名：

```sh
iptables -t filter -L (INPUT/OUTPUT/FORWARD/DOCKER-USER/DOCKER-ISOLATION-STAGE/KUBE-EXTERNAL-SERVICES/KUBE-FIREWALL/UBE-FORWARD/KUBE-KUBELET-CANARY/KUBE-SERVICES)

```

-t选项，查看表名(filter/mangle/nat)
-L 选项，规则/链名
-n 选项，表示不对IP地址进行名称反解，直接显示IP地址。
--line-number 选项， 显示规则的编号

规则大致由两个逻辑单元组成，匹配条件与动作。 


* 测试1：拒绝某个远程主机(10.20.180.12)访问当前主机(10.20.181.132)

```sh
iptables -t filter -I INPUT -s 10.20.180.12  -j DROP
```

 - -I 选项, 插入规则到哪个链
 - -s 选项，匹配条件中的源地址
 - -j 选项，当匹配条件满足，采取的动作


* 测试1.1：拒绝某个远程主机(10.20.180.12)访问当前主机(10.20.181.132)，再追加一条接受(10.20.180.12)的访问

```sh
iptables -A INPUT -s 10.20.180.12 -j ACCEPT
```

 - -A选项，追加规则到某个链。 

不通 即规则的顺序很重要。如果报文已经被前面的规则匹配到，iptables则会对报文执行对应的动作，即使后面的规则也能匹配到当前报文，很有可能也没有机会再对报文执行相应的动作了。


* 测试2: 根据规则编号去删除规则

```sh
iptables --line -vnL INPUT
iptables -t filter -D INPUT N
```

 - -D选项，删除某条链上的第N条规则


* 测试2.2: 根据具体的条件去执行删除规则

```sh
iptables -vnL INPUT
iptables -t filter -D INPUT -s 10.20.180.12 -j DROP
```

修改规则，一般就是删除旧规则，再添加新规则。

* 保存规则

当重启iptables服务或者重启服务器以后，我们平常添加的规则或者对规则所做出的修改都将消失，为了防止这种情况的发生，我们需要将规则"保存"

```sh
iptables-save > /etc/network/iptables.up.rules
iptables-apply #restart iptables 

```

* 更多关于匹配条件

 -s 选项， 指定源地址作为匹配条件，还可以指定一个网段，或用 逗号分割多个IP;  支持取反。

 -d 选项，指定目标地址作为匹配条件。 

不指定，默认就是（0.0.0.0/0），即所有IP

 -p 选项，指定匹配的报文协议类型。

```sh
iptables -t filter -I INPUT -s 10.20.180.12 -d 10.20.181.132 -p tcp -j REJECT
ssh 10.20.180.12 #from 10.20.181.132 ssh t0 10.20.180.12 suppose to be rejected. but not ?
```

 -i选项，匹配报文通过哪块网卡流入本机。

#### iptables之网络防火墙

当外部网络中的主机与网络内部主机通讯时，不管是由外部主机发往内部主机的报文，还是由内部主机发往外部主机的报文，都需要经过iptables所在的主机，由iptables所在的主机进行"过滤并转发"，所以，防火墙主机的主要工作就是"过滤并转发"


![image](http://www.zsythink.net/wp-content/uploads/2017/05/051017_0955_1.png)

主机B也属于内部网络，同时主机B也能与外部网络进行通讯，如上图所示，主机B有两块网卡，网卡1与网卡2，网卡1的IP地址为10.1.0.3，网卡2的IP地址为192.168.1.146: 

![image](http://www.zsythink.net/wp-content/uploads/2017/05/051017_0955_2.png)


c主机网关指向B主机网卡1的IP地址；A主机网关指向B主机网卡2的IP地址。

on hostmachine A:

```sh
route add -net 10.1.0.0/16 gw 192.168.1.146 
ping 10.1.0.1 # ping machine C, not available
ping 10.1.0.3 # ping machine B(NIC 2), avaiailable
```

* 为什么10.1.0.1没有回应。

A主机通过路由表得知，发往10.1.0.0/16网段的报文的网关为B主机，当报文达到B主机时，B主机发现A的目标为10.1.0.1，而自己的IP是10.1.0.3，这时，B主机则需要将这个报文转发给10.1.0.1（也就是C主机），但是，Linux主机在默认情况下，并不会转发报文，如果想要让Linux主机能够转发报文，需要额外的设置，这就是为什么10.1.0.1没有回应的原因，因为B主机压根就没有将A主机的ping请求转发给C主机，C主机压根就没有收到A的ping请求，所以A自然得不到回应

* 为什么10.1.0.3会回应。

这是因为10.1.0.3这个IP与192.168.1.146这个IP都属于B主机，当A主机通过路由表将ping报文发送到B主机上时，B主机发现自己既是192.168.1.146又是10.1.0.3，所以，B主机就直接回应了A主机，并没有将报文转发给谁，所以A主机得到了10.1.0.3的回应


* 如何让LINUX主机转发报文

check `/proc/sys/net/ipv4/ip_forward`. if content is `0`, meaning the Linux hostmachine doesn't forward; if content is `1`, meaning the Linux hostmachine does forward. 

or 

```sh
sysctl -w net.ipv4.ip_forward=1
```

for permenentally allow Linux host forward, update file `/etc/sysctl.conf`. 


设置linux主机转发报文后， A ping C || C ping A should works.


如果我们想要使内部的主机能够访问外部主机的web服务，我们应该怎样做呢？ 我们需要在FORWARD链中放行内部主机对外部主机的web请求.

- 在B主机上：

```sh
iptables -I FORWARD -j REJECT
iptables -I FORWARD -s 10.1.0.0/16 -p tcp --dport 80 -j ACCEPT
```

B主机上所有转发(forward)命令，都REJECT。只ACCEPT 内网10.1.0.0/16 网段， 端口80的转发FORWARD. （即内网网段可访问外网)。 C ping A (ok)

destnation port 目标端口。

想让A ping C, 需在B主机iptables中再添加如下规则：

```sh
iptables -I FORWARD -d 10.1.0.0/16 -p tcp --sport 80 -j ACCEPT
```

source port 源端口。 


配置规则时，往往需要考虑“双向性”。因为一条规则(forward)，只会匹配最新的规则定义。上述修改完了，A 可以PING C，但C又PING不通A了。 a better way, no matter request from in to out or the othersize, both should FORWARD.

```sh
iptables -I FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
```


* 更多动作

NAT, network address translation. 网络地址转换。NAT说白了就是修改报文的IP地址，NAT功能通常会被集成到路由器、防火墙、或独立的NAT设备中。那为什么要修改报文的IP地址呢？


scenario1 :网络内部有10台主机，它们有各自的IP地址，当网络内部的主机与其他网络中的主机通讯时，则会暴露自己的IP地址，如果我们想要隐藏这些主机的IP地址，该怎么办呢？

当网络内部的主机向网络外部主机发送报文时，报文会经过防火墙或路由器，当报文经过防火墙或路由器时，将报文的源IP修改为防火墙或者路由器的IP地址，当其他网络中的主机收到这些报文时，显示的源IP地址则是路由器或者防火墙的，而不是那10台主机的IP地址，这样，就起到隐藏网络内部主机IP的作用。同时路由器会维护一张NAT表，记录这个内部主机的IP和端口。当外部网络中的主机进行回应时，外部主机将响应报文发送给路由器，路由器根据刚才NAT表中的映射记录，将响应报文中的目标IP与目标端口再改为内部主机的IP与端口号，然后再将响应报文发送给内部网络中的主机。

刚才描述的过程中，"IP地址的转换"一共发生了两次。

内部网络的报文发送出去时，报文的源IP会被修改，也就是源地址转换：Source Network Address Translation，缩写为SNAT。

外部网络的报文响应时，响应报文的目标IP会再次被修改，也就是目标地址转换：Destinationnetwork address translation，缩写为DNAT。


不论内网访问外网，Or the otherwise。都会有上述两次IP转换。一般将内网请求外网服务称为snat，外网请求内网服务称为dnat.

上述场景不仅仅能够隐藏网络内部主机的IP地址，还能够让局域网内的主机共享公网IP，让使用私网IP的主机能够访问互联网。比如，整个公司只有一个公网IP，但是整个公司有10台电脑，我们怎样能让这10台电脑都访问互联网呢？ 只要在路由器上配置公网IP，在私网主机访问公网服务时，报文经过路由器，路由器将报文中的私网IP与端口号进行修改和映射，将其映射为公网IP与端口号，这时，内网主机即可共享公网IP访问互联网上的服务了



场景2：公司有自己的局域网，网络中有两台主机作为服务器，主机1提供web服务，主机2提供数据库服务，但是这两台服务器在局域网中使用私有IP地址，只能被局域网内的主机访问，互联网无法访问到这两台服务器，整个公司只有一个可用的公网IP。如何让公网访问到公司的内网服务呢？

将这个公网IP配置到公司的某台主机或路由器上，然后对外宣称，这个IP地址对外提供web服务与数据库服务，于是互联网主机将请求报文发送给这公网 IP地址，也就是说，此时报文中的目标IP为公网IP，当路由器收到报文后，将报文的目标地址改为对应的私网地址，比如，如果报文的目标IP与端口号为：公网IP+3306，我们就将报文的目标地址与端口改为：主机2的私网IP+3306，同理，公网IP+80端口映射为主机1的私网IP+80端口，当私网中的主机回应对应请求报文时，再将回应报文的源地址从私网IP+端口号映射为公网IP+端口号，再由路由器或公网主机发送给互联网中的主机。


###### 测试环境，同ABC主机。

* SNAT 测试

on B hostmachine:

```sh
iptables -t nat -A POSTROUTING -s 10.1.0.0/16 -j SNAT --to-source 192.168.1.146
```

SNAT规则只能存在于POSTROUTING链与INPUT链中。 "--to-source"就是SNAT动作的常用选项，用于指定SNAT需要将报文的源IP修改为哪个IP地址。此处，即B的公网IP.

* DNAT测试

on B machine:

```sh
iptables -t nat -F  #flash nat table 
iptables -t nat -I PREROUTING -d 192.168.1.146 -p tcp --dport 3389 -j DNAT --to-destination 10.1.0.6:3389
```

-j DNAT --to-destination 10.1.0.6:3389"表示将符合条件的报文进行DNAT，也就是目标地址转换，将符合条件的报文的目标地址与目标端口修改为10.1.0.6:3389。 理论上只要完成上述DNAT配置规则即可，但是在测试时，只配置DNAT规则后，并不能正常DNAT，经过测试发现，将相应的SNAT规则同时配置后，即可正常DNAT，于是我们又配置了SNAT:


```sh
iptables -t nat -A POSTROUTING -s 10.1.0.0/16 -j SNAT --to-source 192.168.1.146
```

#### MASQUERADE

当我们拨号网上时，每次分配的IP地址往往不同，不会长期分给我们一个固定的IP地址，如果这时，我们想要让内网主机共享公网IP上网，就会很麻烦，因为每次IP地址发生变化以后，我们都要重新配置SNAT规则，这样显示不是很人性化，我们通过MASQUERADE即可解决这个问题。

MASQUERADE会动态的将源地址转换为可用的IP地址，其实与SNAT实现的功能完全一致，都是修改源地址，只不过SNAT需要指明将报文的源地址改为哪个IP，而MASQUERADE则不用指定明确的IP，会动态的将报文的源地址修改为指定网卡上可用的IP地址。

```sh
iptables -t nat -I POSTROUTING -s 10.1.0.0/16 -o en1 -j MASQUERADE
```

通过B外网网卡出去的报文在经过POSTROUTING链时，会自动将报文的源地址修改为外网网卡上可用的IP地址，这时，即使外网网卡中的公网IP地址发生了改变，也能够正常的、动态的将内部主机的报文的源IP映射为对应的公网IP。

可以把MASQUERADE理解为动态的、自动化的SNAT

#### REDIRECT

使用REDIRECT动作可以在本机上进行端口映射

```sh
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

经过上述规则映射后，当别的机器访问本机的80端口时，报文会被重定向到本机的8080端口上。
REDIRECT规则只能定义在PREROUTING链或者OUTPUT链中。





## refer


[iptables essentials](https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands)

[ip route, ip rule & iptables 知多少](https://cloud.tencent.com/developer/article/1521589)





