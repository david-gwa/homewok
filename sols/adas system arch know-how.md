
## reference 

[vector knowledge Base](https://kb.vector.com/)

[overcoming logging challenges in ADAS dev](https://www.vector.com/int/en/news/news/logging-challenges-adas-sensordata/)


 Up to a million real test kilometers may be driven with a test fleet, depending on the purpose of the vehicles, which corresponds to a logging duration of more than 20,000 hours. Once it is recorded, the logged data can be used any number of times to test new software builds
 
 the primary types of sensors are video cameras, radar sensors and laser scanners (LIDAR). The centerpiece of the ADAS systems is the fusion controller, which takes all sensor data and computes a current environment model in real-time, which is then used to control all drive, steering and braking systems. 
 
 Generally, every sensor manufacturer offers a dedicated logging or debugging solution for their sensors. However, when numerous sensors from different manufacturers are combined in the vehicle, a universal solution is needed that supports all the necessary sensors and stores the data, time-synchronously, in a uniform, standardized format like ASAM-MDF4.
 
 features:
 
 * scalable UI for broad range of user skills
 
 The recordings are labeled to enable better use of the logged data in later work processes



Up to 10 context cameras are used in a vehicle to visually acquire or monitor the driving situation. Each camera generates approx. 60 MByte/s of data, but this data volume can be reduced by up to a factor of 50, using a lossy H.264 video compressor. So this data rate is weighted less as an issue in logging. 

 
[ada logging solution from Vector](https://assets.vector.com/cms/content/events/2019/VA/VECO19/Day_2/ADAS_Data_Logging_Solution_-_Yuchen_Yang.pdf)

 
[confidently record raw ADAS sensor data for drive tests from NI](https://www.ni.com/zh-cn/innovations/automotive/advanced-driver-assistance-systems/adas-datalogger.html)

[online and offline validation of ADAS ECUs](https://assets.vector.com/cms/content/events/2020/Webinars20/Vector_Webinar_Online_Offline_ADAS_ECU.pdf)


[data recording for adas development from Vector](https://assets.vector.com/cms/content/know-how/_technical-articles/ADAS_Recording_Elektronikautomotive_201703_PressArticle_EN.pdf)

[radi vs ssd]()
 
[ssd RAID: boosting ssd performance with RAID](https://www.enterprisestorageforum.com/storage-hardware/ssd-raid.html#:~:text=The%20RAID%20level%20that%20offers%20the%20best%20performance,single%20SSD%2C%20although%20this%20setup%20provides%20no%20redundancy.)

[time sync in automotive Ethernet](https://assets.vector.com/cms/content/know-how/_technical-articles/Ethernet_Timesync_Automobil-Elektronik_201608_PressArticle_EN.pdf)

The principal methods for time synchronization in the automotive industry are currently based on AUTOSAR 4.2.2, IEEE 802.1AS, and the revised IEEE 802.1AS-ref, which was developed by the Audio/Video Bridging Task Group, which is now known as the TSN (Time Sensitive Networking) Task Group.

The type of network determines the details of the synchronization process. For example, with CAN and Ethernet, the Time Slave corrects the received global time base by comparing the time stamp from the transmitter side with its own receive time stamp. With FlexRay, the synchronization is simpler because FlexRay is a deterministic system with fixed cycle times that acts in a strictly predefined time pattern. The time is thus implicitly provided by the FlexRay clock. While the time stamp is always calculated by software in CAN, Ethernet allows it to be calculated by either software or hardware

[mobileye fleets solutions](https://www.mobileye.com/us/fleets/technology/)

[vector support & download](https://www.vector.com/int/en/search/?tx_solr%5Bfilter%5D%5B0%5D=contentType%3Atx_solr_file&tx_solr%5Bsort%5D=datetime+desc&tx_solr%5BresultsPerPage%5D=10)

[QNX platform for ADAS 2.0](https://blackberry.qnx.com/content/dam/qnx/products/adas/adas-product-brief.pdf)


[time sync in modular collaborative robots](https://hackernoon.com/time-synchronization-in-modular-collaborative-robots-d4c218fcb66d)

[solving storage conundrum in ADAS development and validation](https://www.dellemc.com/resources/en-us/asset/white-papers/products/storage/dell-emc-adas-solution-powered-by-isilon-wp.pdf)


[validation of ADAS platforms(ECUs) with data replay test from dSPACE](https://www.dspace.com/en/pub/home/applicationfields/our_solutions_for/driver_assistance_systems/data_driven_development/data_replay/adas-ad_platforms.cfm)

All these components are synchronized by gPTP (generalized Precision Timing Protocol), to ensure synchronous data feed. 

RTMaps, the development framework for multisensor applications from Intempora, supports the synchronous replay of recorded data streams within awide range of file formats, such as MDF4, rosbags, DAT files, etc, in addition to comprehensive 2-D, 3-D visualization capabilities.

[RTMaps from dSpace](https://www.dspace.com/en/pub/home/products/sw/impsw/rtmaps.cfm)

[vADASdeveloper from vector](https://www.vector.com/int/en/products/products-a-z/software/vadasdeveloper/)

[date driven road to automated driving](https://www.microcontrollertips.com/the-data-driven-roadto-automated-driving-faq/)

Data replay offers an excellent way to analyze driving scenarios and verify simulations based on real-world data. This can be done with HIL systems as well as with data logging systems that offer a playback mechanism and software to control the synchronized playback. Captured data can be replayed in real time or at a slower rate to manipulate and/or monitor the streamed data.

An open, end-to-end simulation ecosystem can run scenarios through simulations via a closed-loop process.


[ASAM OpenSCENARIO doc](https://releases.asam.net/OpenSCENARIO/2.0-concepts/ASAM_OpenSCENARIO_2-0_Concept_Paper.html)

[open loop HiL for testing image processing ECUs](https://www.dspace.com/en/pub/home/applicationfields/our_solutions_for/driver_assistance_systems/hil_simulation/open_loop_hil_testing_of_image.cfm#144_35505)



## Autosar time  sync 

[autoSar: time sync protocol specification](https://www.autosar.org/fileadmin/user_upload/standards/foundation/19-11/AUTOSAR_PRS_TimeSyncProtocol.pdf#:~:text=%20%20%20Title%20%20%20Time%20Synchronization,Created%20Date%20%20%2011%2F21%2F2019%2010%3A06%3A48%20AM%20)

Precision Time Protocol (PTP)

generalized Precision Time Protocol (gPTP)

Time Synchronization over Ethernet, IEEE802.1AS


time master: is an entity which is the master for a certain Time Base and which propagates this Time Base to a set of Time Slaves within a certain segment of a communication network. If a Time Master is also the owner of the Time Base then he is the Global Time master. 

time slave: is the recipient for a certain Time Base within a certain
segment of a communication network, being a consumer for this Time Base


time measurement with Switches:

in a time aware Ethernet network, HW types of control unit exists:

* Endpoints directly working on a local Ethernet-Controller

* Time Gateways, time aware bridges, where the local Ethernet-Controller connects to an external switch device.  A Switch device leads to additional delays, which have to be considered for the calculation of the corresponding Time Base


[specification of time sync over Ethernet](https://www.autosar.org/fileadmin/user_upload/standards/classic/4-3/AUTOSAR_SWS_TimeSyncOverEthernet.pdf)

Global Time Sync over Ethernet(EthTSyn) interface with:

* Sync time-base manager(StbM), get and set the current time value

* Ethernet Interface(EthIf), receiving and transmitting messages

* Basic Software Mode Manager(BswM), coord of network access

* Default Error Tracer(DET), report of errors 

 A time gateway typically consists of one Time Slave and one or more Time
Masters.  When mapping time entities to real ECUs, an ECU could be Time Master (or even Global Time Master) for one Time Base and Time Slave for another Time Base.


## Sync Time-base manager 

[CSDN: autosar time sync](https://blog.csdn.net/ChenGuiGan/article/details/103957269)

purpose: 1) sync SW modules; 2) give abs time validation

StbM sends time signals to, 1) triggered customer, 2) active customer, 3) notification customer, 4) go through CAN, FlexRay, Ethernet

全局时间如何通过CAN,FlexRay和ETH来传播? 其实时间同步的难点在于，硬件时钟信号存在偏差

时间矫正算法 Time Deviations Rate Correction :

时间的矫正过程，并不改变各个在本地的运行时钟，而是动态改变本地时钟的实体变量。It merely corrects the clock values on- the-fly when they are read.

CAN Time Synchronization mechanism:

```py 

Global_Time = StbM_GetCurrentTime()

```

[autosar时间同步](https://zhuanlan.zhihu.com/p/41602815)

*Master在t1r时刻先发送一个SYNC信号，但这个信号写的是之前要发送SYNC时的时间点(t0r)，   然后在t2r时刻Slave接收到了这个SYNC信号。

* Master再次发送一个FUP信号，这个信号的内容就是他t1r-t0r的值。

* 最后在Slave方，我们就可以计算出本地当下的同步时间值=(t3r-t2r)+t1r


```sh
检测到障碍物时的全局时间 = 发送Timestamp报文时的全局时间 - （发送Timestamp报文时的局部时间 - 检测到障碍物时的局部时间）
```


[基于autosar的rtos](https://zhuanlan.zhihu.com/p/43760095)

OSEK OS



## topics:

* H264编码 <-- 离散余弦变换（DCT）

* ISO26262

* xcp <-- 应用/标定工程师需要能够在ECU程序运行过程中读取（测量Measure）ECU参数，改变（标定Calibrate）ECU参数的手段。XCP通讯协议就提供了这样一种手段和可能。

* [POSIX标准](https://riptutorial.com/zh-CN/posix),可移植操作系统接口, 它定义了一组标准，以提供不同计算平台之间的兼容性. 当前的POSIX主要分为四个部分：Base Definitions、System Interfaces、Shell and Utilities和Rationale


adas data re-simulation ? 

adas logging solution

time-sync

mobileye TAPI

xcp protocol 

ECU xcp 

Autosar

## Pegasus

FMI, functional mock-up interface 

OSI, open simulation interface   [git](https://github.com/OpenSimulationInterface)



OpenScenario, 

OpenDrive

[sensor models from Pegasus](https://www.pegasusprojekt.de/files/tmpl/Pegasus-Abschlussveranstaltung/20_Sensor_Models.pdf)


[subproject1: scenario analysis and quality measures](https://www.pegasusprojekt.de/en/subproject-1) 

to answer "how good is good enough" 





[Pegasus method: an overview pdf](https://www.pegasusprojekt.de/files/tmpl/Pegasus-Abschlussveranstaltung/PEGASUS-Gesamtmethode.pdf)


[pegasus method web link](https://www.pegasusprojekt.de/en/pegasus-method)


































 
 
 
 
 
 