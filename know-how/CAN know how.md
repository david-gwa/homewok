
## CAN network protocols 

* 物理层:  总线电平、消息编码、 位定时/构建、同步、 CAN控制器、CAN网络拓扑、波特率与总线长度

* 数据链路层： 总线访问仲裁、帧格式、错误检测、错误处理、协议版本

* CAN收发器负责逻辑电平和(差分)信号电平之间的转换。网络链路层

* CAN总线采用不归零码位填充。CAN总线上的信号有两种不同的信号状态，dominant(显性)逻辑0， recessive(隐性)逻辑1，信号每一次传输完不需要返回到逻辑0

```
CAN_H - CAN_L < 0.5V，CAN 总线表现为隐性，逻辑信号为1，高电平；
CAN_H - CAN_L > 0.9V, CAN 总线表现为显性，逻辑信号为0，低电平。
```

* "线与"

```sh
1&0 = 0 
```

即总线上只要有一个节点为低电平(逻辑0)/显性状态，CAN总线即为低电平。只有当所有节点都为高(隐性)，总线才为高(隐性)





## CAN matrix 

[如何理解CAN通信矩阵](https://zhuanlan.zhihu.com/p/62333363)

CAN通信矩阵（CAN Communication Matrix）通常由整车厂完成定义，车辆网络中的各个节点需要遵循该通讯矩阵才能完成信息的交互和共享。

对于乘用车来说，满足UDS和尾气排放协议之后，还剩余了绝大部分的ID段。这些ID段由主机厂自主来进行分配，分配好之后会形成一个.xls格式的表格。有了CAN通信矩阵，开发人员就知道他设计的零部件应该接收什么ID的数据，需要发出什么ID的数据。


* 信号名称
* 信号长度
* 精度/偏移量
* 物理值范围
* 起始值范围
* 起始字节
* 起始位: least significant bit(LSB)
* 信号类型(boolean or unsigned)


-- most significant bit(MSB)， 信号高位，即权重大的位。

-- least significant bit(LSB)，信号低位，即权重低的位。其变化，对信号值影响不大

如何将数据矩阵中的内容对应到8x8的格子中，就是CAN矩阵的关键。

填充时是从右向左填充的，信号起始从右侧填入LSB。

如果你的Signals都没有跨字节(8位)的问题，那么Intel和Motorola格式出来的效果是一样的。


* Intel格式 (小端)

MSB在LSB下一行

* Motorola格式(大端)

MSB在LSB上一行



##### CAN 信号结构

[CAN的通讯](https://zhuanlan.zhihu.com/p/137064965) 和LIN其实都是基于帧的. 这一个显性电平的发出也代表着一帧信号的开始。

发送节点在发送数据时会把计算的校验值写到CRC段，接收节点在接收数据时，会在接收节点以同样的CRC校验方式进行计算，然后比对自己的计算结果和接收的计算结果，以判断数据在传输的过程中是否出现了位丢失或者其它位错误的情况，是一种通讯安全的机制。

[can 通讯效验](https://zhuanlan.zhihu.com/p/143794890)

在 CAN 协议中，所有的消息都以固定的格式发送。

##### CAN通讯的一些特点

它是一种多主总线，即每个节点机均可成为主机，且节点机之间也可进行通信。

通信介质可以是双绞线，通信速率最高可达1mb/s。

CAN总线通信接口中集成了CAN协议的物理层和数据链路层功能，可完成对通信数据的成帧处理，包括位填充、数据块编码、循环冗余校验、优先级仲裁等项工作。

数据段长度最多为8个字节，可满足通常工业领域中控制命令、工作状态及测试数据的一般要求。同时，8个字节不会占用总线时间过长，从而倮证了通信的实时性。

CAN协议采用crc检验并可提供相应的错误处理功能，保证了数据通信的可靠性。CAN总线所具有的卓越性能、极高的可靠性和独特设计，特别适合工业设备测控单元互连。因此备受工业界的重视，并已公认为最有前途的现场总线之一。

#### 举例 

仪表想要获取这个发动机的转速信息只能跟发动机的ECU去索取。通讯信号是最好的载体，可以表达更多的可能性，比如一个10位长度的信号可以有1024种可能性，就算你想把信息表达到10000，分配14位的信号足够了。一帧CAN消息就可以装载8字节(64位)的消息。

![image](https://pic3.zhimg.com/80/v2-245923c3f303d54cd969c6a52457551e_720w.jpg)

![image](https://pic2.zhimg.com/80/v2-f34bc6f807757c5732d29362260268f0_720w.jpg)



如果CAN线上有很多的数据，作为一个节点怎么知道哪些是需要读取的，哪些是不需要的呢，这个就是在车辆开发的时候就已经定义的，对应的节点需要订阅哪些消息是固定的，都是根据功能设计的，然后通过CAN的ID识别自己需要的数据即可。


[如何进行汽车CAN总线开发](https://www.zhihu.com/question/35630289)


### DBC

[dbc 到底是个啥](https://zhuanlan.zhihu.com/p/141638034) 

database Can, CAN网络的通讯就是依据这个文件的描述进行的，因为有了它才可以使得整个CAN网路的节点控制器无差错的协同同步开发。

* 创建数值表的意义是为了给后续创建的信号提供解释, 因为数值表中对数值含义的解释可以完成对信号含义的解释

* 创建signal，，在value table 的位置选择我们在上一步建立的数值表，这样就将信号和数值表链接起来了，同时也完成了信号的创建。

* 创建message。CAN通讯的载体是帧，也就是消息，而不是单纯的一个一个的信号，是把很多的信号封装到消息帧里面以帧的格式进行传输的，所以在建立了signal之后还需要将信号封装到帧中，那么就需要首先创建message。在message中则需要定义清除帧的ID是多少，帧的类型，帧的长度，由哪个节点发送，发送的周期是多少等等


* 创建网络节点。定义消息的时候需要有发送的节点，那么这个节点就是CAN通讯中的网络节点

总结，简单的讲，dbc文件描述了在CAN网络上有哪些报文信息；这些报文上又携带了哪些信号信息；该报文是从哪个节点发出，哪个节点进行接收的等信息。



#### [CAN控制器与收发器](https://zhuanlan.zhihu.com/p/151073146)

![image](https://pic1.zhimg.com/80/v2-c5b1f7a91ad96c38c999f1743751b805_720w.png)

#### [不同格式CAN相互转化](https://zhuanlan.zhihu.com/p/147095521)

can matrix中的信号如果比较少可以用CANdb++手动编辑


[canMatrix](https://github.com/ebroecker/canmatrix/tree/development/src/canmatrix)


#### [DBC格式](https://zhuanlan.zhihu.com/p/141408513)


physical_value =  raw_value * factor + offset 

raw_value = (physical_value - offset) / factor 



#### [CANoe 仿真](https://zhuanlan.zhihu.com/p/209056758)


CAN IG(Interactive Generator) 模块用来向总线发送用户自定义或数据库中的报文.

IG can be used to send messages as well as to set the corresponding signal values.




#### [Testing ECUs and networks with CANoe](https://www.vector.com/int/en/products/products-a-z/software/canoe/)


CANoe 用来对CAN通信网络进行建模、仿真、测试和开发。


## CANoe manual

[pdf](https://assets.vector.com/cms/content/products/canoe/canoe/docs/Product%20Informations/CANoe_ProductInformation_EN.pdf)

the data flow from data source to its display or logging 


## CANoe Matlab/Simulink integration 

* HiL or online mode, code generated from Simulink, added as a DLL at a simulated node in CANoe 

* In offline mode, the two programs are coupled. Simulink provides the time base, and CANoe is in Slave mode. The entire system operates in simulated mode. It is not possible to access real hardware here.



## Test ECUs and Networks 


## Diagnostics 

CANoe supports both the implementation and testing of diagnostics functionality by providing access to the diagnostic interfaces of ECUs



## CAPL programming 

* event-oriented control 

| event | handler| 
|----|----|
| time controlled   | on_timer   |   
| message IO   | on message ESPStatus  |   
| on signal update   | rewrites signal vals   |   



### Panels 














## 参考

[CAN总线要点](https://www.cnblogs.com/spoorer/p/6649303.html)

