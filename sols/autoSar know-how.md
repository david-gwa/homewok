


[11 Time sync](https://blog.csdn.net/sky8336/article/details/91355471)


对于自适应平台，考虑了以下三种不同的技术来满足所有必要的时间同步需求：

* 经典平台的StbM

* 库chrono -要么std::chrono (c++ 11)，要么boost::chrono

* 时间POSIX接口


TBRs充当时间基代理，提供对同步时间基的访问。通过这样做，TS模块从“真实的(real)”时基提供者中抽象出来。


[04 OS](https://blog.csdn.net/sky8336/article/details/91126937)

操作系统(OS)负责自适应平台上所有应用程序的运行时调度、资源管理(包括管理内存和时间限制)和进程间通信。


[03 Archtecture](https://blog.csdn.net/sky8336/article/details/90766173)

一种是“基于库”的设计；另一种是“基于服务”的设计。

如果只在本地的AP实例中使用它，那么基于库的设计更合适，因为它更简单，也更高效。如果以分布式方式从其他AP实例使用它，建议使用基于服务的设计作为通信，无论客户端AA和服务位于何处，管理都提供透明的通信

AUTOSAR平台的软件组件，它们将在一个单一模型的单个系统中使用。不同AUTOSAR平台的软件组件可以以面向服务的方式彼此通信。


[05 Execution Management](https://blog.csdn.net/sky8336/article/details/91127246)

[06 State management](https://blog.csdn.net/sky8336/article/details/91135955)

[07 communication management]()



## [autosar: 微控制器抽象层 MCAL](https://blog.csdn.net/ChenGuiGan/article/details/80310713)

#### 微控制器驱动

* GPT Driver

* WDG Driver

* MCU Driver 

* Core test 

#### 存储器驱动

#### 通信驱动

* Ethernet驱动

* FlexRay 驱动

* CAN 驱动

* LIN 驱动

* SPI 驱动

#### I/O驱动


## [AUTOSAR：基础软件层](https://blog.csdn.net/ChenGuiGan/article/details/80305190)


AUTOSAR软件体系结构包含了完全独立于硬件的应用层（Application Layer）和与硬件相关的基础软件层（BasicSoftware,BSW），并在两者中间设立了一个运行时环境（Run Time Environment），从而使两者分离，形成了一个分层体系架构。

#### 基础软件层组件

* 系统，提供标准化(os, timer, error)规定和库函数

* 内存，对内、外内存访问入口进行标准化

* 通信，对汽车网络系统、ECU间、ECU内的通信访问入口进行标准化

* I/O， 对传感器、执行器、ECU的IO进行标准化

#### 基础软件层模块

* 驱动模块，包括内部驱动、外部驱动 

* 接口模块，



## [服务层与复杂驱动](https://blog.csdn.net/ChenGuiGan/article/details/80380054)

#### 系统服务

比如， os定时服务、错误管理。为应用程序和基础软件模块提供基础服务。

#### 存储器服务

#### 通信服务

通信服务通过通信硬件抽象与通信驱动程序进行交互

#### 复杂驱动

复杂驱动（CCD）层跨越于微控制器硬件层和RTE之间，其主要任务是整合具有特殊目的且不能用MCAL进行配置的非标准功能模块。复杂驱动程序跟单片机和ECU硬件紧密相关。

[autosar com stack 介绍](https://www.sohu.com/a/217591212_467757)

## [AUTOSAR现状与利弊](https://blog.csdn.net/ChenGuiGan/article/details/84335207)


## [AUTOSAR time sync](https://blog.csdn.net/ChenGuiGan/article/details/103957269)

为了统一控制时间，我们就需要一个全局时间软件模块(StbM, Synchronized Time-base Manager)。

功能只有两个:1. 同步各个软件模块实体，2. 提供绝对时间值。

时间同步的难点在于，硬件时钟信号存在偏差。




