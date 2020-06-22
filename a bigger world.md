
[disque](https://github.com/antirez/disque)


分布式共识算法

一致性哈希

**[分布式一致性与共识算法](https://draveness.me/consensus/)


[https://draveness.me] is a very good blog

zookeeper vs  etcd 

etcd 集群的工作原理基于 raft 共识算法

使用 etcd 实现微服务架构中的服务发现、发布订阅、分布式锁以及分布式协调等功能


[etcd: why gRPC gateway](https://etcd.io/docs/v3.4.0/dev-guide/api_grpc_gateway/)





[linux运维之美](https://www.hi-linux.com/) is a very good blog 



[design ros2: topological discovery and communication negotiation](https://design.ros2.org/articles/discovery_and_negotiation.html), need do some research about ros2 design logic and answer this hidden logic of ros protocol


## ros 


[古月居 ros产品化：通信机制](https://www.guyuehome.com/1641)

点对点的分布式通信机制是ROS的核心，使用了基于TCP/IP的通信方式，实现模块间点对点的松耦合连接，可以执行若干种类型的通信，包括基于话题（Topic）的异步数据流通信，基于服务（Service）的同步数据流通信，还有参数服务器上的数据存储等

#### [ros on DDS](https://design.ros2.org/articles/ros_on_dds.html)

* discovery 

DDS, dynamic discovery system, DDS would completely replace the ROS master based discovery system. The advantage of the DDS discovery system is that, by default, it is completely distributed, so there is no central point of failure.  DDS also allows for user defined meta data in their discovery system, which will enable ROS to piggyback higher level concepts onto publish-subscribe.


* publish-subscribe transport 

The DDSI-RTPS (DDS-Interoperability Real Time Publish Subscribe) protocol would replace ROS’s TCPROS and UDPROS wire protocols for publish/subscribe.


* transpot alternatives 

In the context of DDS, most vendors will optimize message traffic (even between processes) using shared-memory in a transparent way, only using the wire protocol and UDP sockets when leaving the localhos


* messages 

Much of the semantic contents of current ROS code is driven by the structure and contents of these messages, so preserving the format and in-memory representation of the messages has a great deal of value. In order to meet this goal, and in order to make DDS an implementation detail, ROS 2 should preserve the ROS 1 like message definitions and in-memory representation.

This ratio between the cost of converting types and the cost of serialization, which was found to be at least one order of magnitude. 


`intraprocess communication` in ROS would not use the DDS in-memory representation so this field-by-field copy would not be used unless the data is going to the wire. 
 

#### stories driving ros2 dev 

the ROS1 communication between the nodes and the master is done using XML-RPC which poses a significant dependency when being implemented on small resource constraint systems / micro controllers due to its recursive unbounded nature. 
 
implement the ROS protocol directly on the devices embedded system. The adoption of an industry standard like DDS as well as the decentralized nature of the middleware are important pieces to enable this.

`nodelet` ?

In ROS 1 the launch system is only able to start a set of processes. It doesn’t provide any more feedback beyond the information if a process has finished




 
 
 

