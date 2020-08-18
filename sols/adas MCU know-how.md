

## MCU tc0 定时器

[Infineon AURIX ](https://www.infineon.com/dgdl?fileId=5546d4615bd7187f015bf30cea630233)

[非周期、事件型数据的存储方式](https://zhuanlan.zhihu.com/p/146514545)


## FreeRTOS 

[空闲任务与阻塞延时](https://blog.csdn.net/dingyc_ee/article/details/100555016)

[设计定时任务系统](https://developer.51cto.com/art/202008/623049.htm)

* 任务录入

* 任务调度

* 任务执行




## SPI 协议

SPI, Serial Peripheral Interface。使MCU与各种外围设备以串行方式进行通信以交换信息。
SPI总线可直接与各个厂家生产的多种标准外围器件相连，包括FLASHRAM、网络控制器、LCD显示驱动器、A/D转换器和MCU等。

SPI接口主要应用在EEPROM、FLASH、实时时钟、AD转换器， ADC、 LCD 等设备与 MCU 间，还有数字信号处理器和数字信号解码器之间，要求通讯速率较高的场合。


## TAPI协议

TAPI（电话应用程序接口）是一个标准程序接口，它可以使用户在电脑上通过电话或视频电话与电话另一端的人进行交谈。TAPI还具备一个服务提供者接口（SPI），它面向编写驱动程序的硬件供应商。TAPI动态链接库把API映射到SPI上，控制输入和输出流量。 





## MCU 非周期任务  定时任务

实时任务分类：周期任务、偶发任务、非周期任务 

[嵌入式系统的定义](https://zhuanlan.zhihu.com/p/66347224)


[scheduling sporadic and aperiodic events in a hard real-time system](https://pdfs.semanticscholar.org/926b/1a5e44a87bdaa979e98608650821fa35f79c.pdf)


A common use of periodic tasks is to process sensor data and update the current state of the real-time system on a regular basis. 

 Aperiodic tasks are used to handle the processing requirements of random events such as operator requests. An aperiodic task typically has a soft deadline. Aperiodic tasks that have hard deadlines are called sporadic tasks.
 
 Background servicing of aperiodic requests occurs whenever the processor is idle (i.e., not executing any periodic tasks and no periodic tasks are pending).  If the load of the periodic task set is high, then utilization left for background service is low, and background service opportunities are relatively infrequent. However, if no aperiodic requests are pending, the polling task suspends itself until its next period, and the time originally allocated for aperiodic service is not preserved for aperiodic execution but is instead used by periodic tasks
 
 
 
 
 
## [foreground-background scheduling](https://www.geeksforgeeks.org/foreground-background-scheduling/)
 
 * periodic tasks are considered as foreground tasks
 
 * sporadic and aperiodic tasks are considered as background tasks
 
 foreground tasks have the highest priority and the bc tasks have lowest priority. among all highest priority, the tasks with highest priority is scheduled first and at every scheduling point, highest priority task is scheduled for execution. only when all foreground tasks are scheduled, bc task are scheduled. 
 
 * completion time for foreground task
 
for fg task, their completion time is same as the absolute deadline.

* completion time for background task 

when any fg task is being excuted, bc task await.

let Task **Ti** is fg task, **Ei** is the amount of processing time required over every **Pi** period. Hence，

```
Avg. CPU utilization for Ti is Ei/Pi 

```

if there are **n** periodic tasks(fg tasks), e.g. T1, T2, ... Tn 

then total avg CPU utilization for fg taskes:

```
fg_cpu_util = E1/P1 + E2/P2 + ... + En/Pn
```

then the avg time available for execution of bg task in every unit of time is:

```
1 - fg_cpu_util
```
 
let **Tb** is bg task, **Eb** is the required processing time, then the completion time of bg task:

```
=  Eb / (1 - fg_cpu_util)
```


in ADAS system, usually there exist bost periodic tasks(fg) and aperiodic tasks(bc), and they are corelated, fg tasks always have higher priority than bc tasks. so there is chance when a certain fg task rely on output of another bc task, which is not or partially updated due to executing priority, then there maybe some isues.




## [Functional safety and ECU implementation](https://assets.vector.com/cms/content/events/2019/VH/VIC2019/Track_4_3_Functional_Safety_and_ECU_Implementation.pdf) from Vector 

#### SafeOS 

* what faults are possible ? 

memory violations -->  memory partition, stack protection 

timing violations  -->  timing protection 

#### timing protection 

* execution budgets are assigned to task and monitored


## [autosar OS measures task execution times](https://www.eetimes.com/autosar-os-measures-task-execution-times/)

Software design is easy when the processor can provide far more computing time than the application needs. 







## [3min看懂mcu](https://www.sohu.com/a/298859329_257861)

要了解一款MCU，首先需要知道就是其ROM空间、RAM空间、IO口数量、定时器数量和定时方式、所提供的外围功能模块（Peripheral Circuit）、中断源、工作电压及功耗等

基本功能：

* Timer

包括固定时间间隔的timer和可编程定时器(programmable timer)。 由于时钟源可以自由选择，因此，此类Timer一般均与Event Counter(事件计数器)合在一起。

* IO

* 通讯接口

SPI接口，其数据传输采用同步时钟来控制。谁提供时钟信号，提供时钟的一方为Master，相反的一方则为Slaver。





## keywords 

* SPI 

* ADSL, 数字用户线路。各信号之间采用频分复用方式占用不同频带，低频段传送话音；中间窄频带传送上行信道数据及控制信息；其余高频段传送下行信道数据、图像或高速数据

[嵌入式系统基础知识总结](https://www.eet-china.com/mp/a22986.html)

* mobileye














