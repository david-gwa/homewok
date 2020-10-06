## background 

this is a time to answer the base logic of simulation in autonomous driving(AD).

before this happens, we had went through at least the following steps:

* ADAS L2 sim

most traditional commercial sims, e.g. vtd, prescan e.t.c. 

* L3+ WorldSim

when the top consulting company say to get a safety AD, the AD requirest 10 billion miles verification, we jump into LGSIM, CarLA, to get shoes wet about the game engine based simulator. there are some funny works, and a good try to deploy in cloud, but still far away from product services 

* L2 LogSim

when we deploy LogSim system, to assist ADAS L2 algorithm iteration and validation. the logic of logSim is clear: for L2 ADAS development, during the development cycle, there are about 5 major versions, a few minor versions in each major version, to validate all these versions update function well, we can first test with standard scenarios in ADAS L2 sim, e.g. PreScan, which is enough for ADAS L2 to satisfy the least requirements; only for few statical performance, e.g. AEB false positive performance, it depends much on LogSim. 

what else can LogSim provide, e.g. to optimize a better functional performance ?


so now we come to the question, why we need simulation during AD development and even after massively produced ? how to close loop simulation toolchain with AD data pipleine ? and to answer this, we need first answer what's the benefit or value of simulation ?


 what's the best understanding of simulation from AD simulation teams ?

## [QCraft](https://www.qcraft.ai/)

Our mission at QCraft is to bring autonomous driving into real life by using [a large-scale intelligent simulation system and a self-learning framework for decision-making and planning](https://www.qcraft.ai/1852273-1862545.html?newsid=1816799&_t=1582550990).



QCraft was ex-waymo simulation team, has a solid understanding about simulation in AD R&D. 

the logic behind QCraft: 

* 感知是一个比较确定性的问题，如何测试和评价是非常明确的，整体的方法论也是比较清楚的

* 规划决策视为目前最具挑战性的问题。第一，不确定性难以衡量。现有判断规划决策做得好坏的指标是舒适度和安全性；第二，从方法论的角度来说，行业里占主流位置的规划决策方法论，整体上看与20年前相比并没有大的突破。模仿学习或强化学习的方法，在大规模实际应用时也仍然存在众多问题


许多创业公司从无到有的技术构建过程——先做好建图和定位，再做好感知，最后再开始做规划决策和仿真。

边界化难题（Cornercase），在你遇上野鸭子之前，你甚至不知道会有野鸭子的问题，所以边界化难题是需要有方法去(自动)发现新的corner case，并解决。

除了收集大量的数据，更重要的是建立自动化生产的工厂，将源源不断收集来的有效数据，通过自动化的工具，加工成可用的模型。以更快的速度、更高效的方式应对边界化难题（Corner case）。

测试工具是为了帮助工程师高效地开发，快速复现车辆上的问题，并提前暴露可能的潜在问题，同时也是提供一个评估系统，评价一个版本和另外一个版本比是变好了还是变坏了。

我们的测试系统可做到和车载系统的高度一致，在路上出现的问题，回来就能在仿真里复现，并进行修复。保证再次上路时不出现同样问题。我们产生的场景库也与现实环境高度一致，因为本来就是从现实中学习来的

轻舟智航不希望“只见树木不见森林”——通过见招拆招的方式进入到某个具体的小应用场景，变成一家靠堆人来解决问题、无法规模化的工程公司，

#### [QCraft: 实现无人驾驶需要什么样的仿真系统](https://www.qcraft.ai/1852273-1862545.html?newsid=1816797)

* 基于游戏引擎开发的仿真软件大都“华而不实”

仿真软件在自动驾驶领域的重要应用，就是复现(replay)某一次的路测效果。但由于这种第三方软件的开发与自动驾驶软件的开发是相互独立的，很难保证其中各个模块的确定性，导致整个仿真软件存在不确定性，最终影响可用性。


轻舟智航仿真系统的系统架构可以分为5层：最底层的是轻舟智航自研的Car OS，借助底层的通讯系统来保证模块之间的高效通讯； Car OS与仿真器是高度整合的系统，核心仿真器及评估器，是基于底层的Car OS接口开发的，能保证仿真系统的确定性；再往上一层是仿真周边工具链和基础架构，可保证整个数据闭环的有效性，将全部数据高效利用起来；第四层是大规模场景库构建；最顶层则是分布式系统仿真平台，支持快速、大规模的仿真应用，在短时间内得出正确评估。

仿真场景库的自动生成的相关工作。视频中红色和绿色的两个点，分别代表两辆车的运动轨迹，这些轨迹的生成和变化，是在真实的交通数据集上，利用深度学习的方法进行训练，再使用训练好的深度神经网络 (生成模型) 合成大规模的互动车辆的轨迹

我们认为仿真是达到规模化无人驾驶技术的唯一路径。首先，借助仿真及相关工具链，能形成高效的数据测试闭环，支持算法的测试和高效迭代，取代堆人或堆车的方式；其次，只有经过大规模智能仿真验证过的软件，才能够保证安全性和可用性。


## [Latent Logic](https://www.latentlogic.com/) 

another waymo simulation startup, offers a platform that uses **imitation learning** to generate virtual drivers, motorists and pedestrians based on footage collected from real-life roads. Teams working on autonomous driving projects can insert these virtual humans into the simulations they use to train the artificial intelligence powering their vehicles. The result, according to Latent Logic, is a closer-to-life simulated training environment that enables AI models to learn more efficiently.


#### [training autonomous vehicles using real-life human behaviour](https://www.research.ox.ac.uk/Article/2019-06-19-training-autonomous-vehicles-using-real-life-human-behaviour)


‘Autonomous vehicles must be tested in simulation before they can be deployed on real roads. To make these simulations realistic, it’s not enough to simulate the road environment; we need to simulate the other road users too: the human drivers, cyclists and pedestrians with which an autonomous vehicle may interact.'

‘We use computer vision to collect these examples from video data provided by traffic cameras and drone footage. We can detect road users, track their motion, and infer their three-dimensional position in the real world. Then, we learn to generate realistic trajectories that imitate this real-life behaviour.’

## [Roman Roads](https://www.romanroads.io/)

using **imitation learning** to train robots to behave like human, state of the art behavioral tech.

We offer **R&D solutions** from 3D environment creation, traffic flow collection to testing & validation and deployment.

* driving behavior data collection 

ego view collection, fleet road test 


* real-time re-construction

real time generation of 3d virtual env and human behavior(imitation learning)


* data-driven decision making 


* pre-mapping 

The behavior offset are different between two cities. We collect data, like how people change lane and cut in, and learn the naturalistic behaviors at different cities.


I have to say this is a very solid AI team, and if OEM can integrate this solution into their data close-loop platform, namely this is the flying wheel to power the AD system like Tesla.


## [Cognata](https://www.cognata.com/)

Hyundai Mobis simulation tool. 

Cognata delivers large-scale full product lifecycle simulation for ADAS and Autonomous Vehicle developers.  

#### training

Automatically-generated 3D environments, digital twins or entirely synthetic worlds by DNN, synthetic datasets, and realistic AI-driven traffic agents for AV simulation.


#### validation 

* pre-built scenarios, 

* standard ADAS/AV assessment programs 

* fuzzing for scenario variaties for regulations and certifications 

* UI friendly 

#### analysis 

* Ready-to-use pass/fail criteria for validation and certification of AV and ADAS

* Trend mining for large scale simulation

#### visulization


### how it works 

static layer: digital twin 

dynamic layer: AI powered vehicles and pedestrains 

sensor layer: most popular sensor models based on DNN 

cloud layer: 


Cognata as an independent simulation platform is so good, but when considering integration with exisitng close loop data platform in OEMs, it's like a USA company, too general, doesn't wet the shoe deeply, compare to QCraft, the sim architecture is from down to top, from car OS to cloud deployment, which is more reliable solution for massively ADAS/AD products in future.

## [applied intuition](https://www.appliedintuition.com/)

another Waymo derived simulation company. 

Test modules individually or all together with our simulation engine that’s custom built for speed and accuracy.

improve perception algorithms, Compare the performance of different stack versions to ground truth data.

Test new behaviors and uncover edge cases before pushing updates to your vehicles.

* Extract valuable data from real world drives and simulations

* Review interesting events recorded from vehicles and simulations to determine root cause issues. Share the data with other team members for further analysis and fixes.

* Extract and aggregate performance metrics from drive logs into automatic charts, dashboards, and shareable reports for a holistic view of your development progress.

* Run your system through thousands of virtual scenarios and variations to catch regressions and measure progress before rolling it out for on-road testing.


looks pretty.


## [metamoto](https://www.metamoto.com/)

simulation as a service, Enterprise products and services for massively scalable, safe, scenario-based training and testing of autonomous system software

it's an interet based simulator compare to preScan, but in core is just another preScan, with additionaly scalability. can't see data loop in the arch. so it's helpful during R&D, but not realy usefuly after release.





## [Parallel Domain](https://paralleldomain.com/)

power AD with synthetic data, the ex-Apple AD simulation team.


Parallel Domain claims its computing program will be able to generate city blocks less than a minute, Using real-world map data.  Parallel Domain will give customers plenty of options for fine tuning virtual testing environments. The simulator offers the option to incorporate real-world map data, and companies can alter everything from the number of lanes on a simulated road to the condition of its computer-generated pavement. Traffic levels, number of pedestrians, and time of day can be tweaked as well.

[Nio is the launch customer of Parallel Domain](https://www.thedrive.com/tech/20559/parallel-domain-wants-to-create-a-virtual-world-for-self-driving-car-tests)

[PD looks to train AD in virtual reality](https://www.futurecar.com/2229/Parallel-Domain-Looks-to-Train-Autonomous-Vehicles-in-Virtual-Reality)

**from real map to virtual world**, and road parameters are programable. but what about micro traffic flow, vehicle-pedestrain-cars interaction ?

I think it's great to generate virtual world with Parallel Domain, but not enough as the simulator in the whole close loop.

the collected data, of course include real map info, which can used to create virtual world, but why need this virtual world? is to train AD P&C system, which is more than just the static virtual world and with some mimic pedestrain/vehicle behaviors.

in AI powered AD, valid and meaningful data is the oil. the basic understanding here is to with more data, get more robost and general AI model, which means with more data, the AI AD system can do behavior better with existing scenarios, and more importantly, do increase the ability to handle novel scenarios automatically.

so is the close loop data in AD.


## [righthook](https://righthook.io/how-it-works/)

* digital twin of real world 

* scenario creation tool powered by AI

 to derive high-value permuation and test cases automatically(maybe both static and dynamic scenarios)

* vehicle configuration 


* test management 

integration with DevOps and cloud on-premise 


in a world, this is something similar like Cognata, to generate vivid world from physical map data or synthetic data, then add imitation learning based agents, then a DevOps tool and web UI configurable.

the most important and also the difficult part of this pipeline, is how to obtain large mount of valid and useful real data as cheap as possible, to train the scenario generator, as well as agents behavior generator. 

only MaaS taxi companies and OEMs have the data. 



## [rfpro](http://www.rfpro.com/)

a driving simulation and digital twin for ad/adas, vd(chassis, powertrain e.t.c) development, test and validation. 


 rFpro includes interfaces to all the mainstream vehicle modelling tools including CarMaker, CarSim, Dymola, SIMPACK, dSPACE ASM, AVL VSM, Siemens Virtual lab Motion, DYNAware, Simulink, C++ etc.  rFpro also allows you to use industry standard tools such as MATLAB Simulink and Python to modify and customise experiments.

rFpro’s open Traffic interface allows the use of Swarm traffic and Programmed Traffic from tools such as the open-source SUMO, IPG Traffic, dSPACE ASM traffic, PTV VisSim, and VTD. Vehicular and pedestrian traffic can share the road network correctly with perfectly synchronised traffic and pedestrian signals, while allowing ad-hoc behaviour, such as pedestrians stepping into the road.

[data farming: generating mimic training data](http://www.rfpro.com/driving-simulation/datafarming/)



* the largest lib of digital twins of public roads in the world 

* supervised learning env for perception 





## [edge case research](https://edge-case-research.com/)

#### Hologram 

complements traditional simulation and road testing of perception systems

Hologram unlocks the value in the perception data that’s collected by your systems.  It helps you find the edge cases where your perception software exhibits odd, potentially unsafe behavior.

from recorded data, to automated edge case detection(powered by AI), The result: **more robust perception**

![image](https://edge-case-research.com/wp-content/uploads/2019/07/image.png)


![image](https://ecrweb.wpengine.com/wp-content/uploads/2018/08/Web-1920-%E2%80%93-1@2x.png)

most of the cost of developing safety-critical systems is spent on verification and validation. 

in a world, is ECR to verify and valiate AD safety requirements? 


## [foretellix](https://www.foretellix.com/adas-and-highway-solution/)

out of box verification automation solution for ADAS and highway functions, developed based on input from OEMs, regulators and compliance bodies. 

**Coverage Driven Verification**, Foretellix’s mission is to enable **measurable safety** of ADAS & autonomous vehicles, enabled by a transition from measuring ‘quantity of miles’ to ‘quality of coverage’ 


[how it works](https://www.foretellix.com/technology/)


* what to test ?

Industry proven verification plan and 36 scenario categories covering massive number of challenges and edge cases

* When are you done?

Functional coverage metrics to guide completeness of testing


![image](https://www.foretellix.com/wp-content/uploads/2020/08/Untitled-design-47.png)

this is ADAS L2 V&V solution, mostly in functional metric test. 



#### [Open Language: M-SDL](https://www.foretellix.com/open-language/)

M-SDL is an open, human readable, high level language that allows to simplify the capture, reuse and sharing of scenarios, and easily specify any mix of scenarios and operating conditions to identify previously unknown hazardous core & edge cases. It also allows to monitor and measure the coverage of the autonomous functionality critical to prove  ADAS & AV safety, independent of tests and testing platforms. 

![image](https://www.foretellix.com/wp-content/uploads/2019/09/new%E2%80%94screen_REPLACEMENT.jpg)




## [atlatec](https://www.atlatec.de/simulation.html)

HD map for simualtion, digitial twin of real road, integrated well with simulation suppliers, e.g. IPG, Vires, Prescan.







## [ivex](https://ivex.ai/)

provides **qualitatively safety assessment of planning and decision making** for all levels of ADs during development. 

#### [safety assessment tool](https://ivex.ai/assessment_tool/) 

what is safety requirements during AD development ?

what's the KPIs to represent these safety requirements ? 

is safety requirements iterative in each functional iteration, or done once for ever ?

safety requirements can be validate before release, after then, when new corner cases detected, need to do safety validate automatically. so in this way, safety and function should keep in the same step.

the ability of safety assessment tool :

* unsafe cases and decision detection from a large amount of scenarios 

* a qualitative metric of safety (RSS model)

* statistical analysis of risk and safety metrics 



#### [safety co-pilot](https://ivex.ai/safety_copilot/)

guarantee safety of a planned trajectory. 

The safety co-pilot uses the safety model to assess whether (1) a situation is safe, and (2) a planned trajectory for the next few seconds can be considered as safe, accounting for predicted movements of other objects and road users.


in a word, safety is big topic, but I can't see the tech behind how Ivex solve it.



## [nvidia](https://www.nvidia.com/en-us/self-driving-cars/)

## [intel](https://www.intel.com/content/www/us/en/automotive/autonomous-vehicles.html)







## refer 

[SelfDriving.fyi](https://selfdriving.fyi/)


[north america incubator](https://www.naincubator.com/)














 
