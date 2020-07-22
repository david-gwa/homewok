
## Verification and Validation in V-model


#### verification 

* whether the software conforms the specification 
* finds bugs in dev 
* output is software arch e.t.c 
* QA team does verification and make sure the software matches requirements in SRS.
* it comes before validation 


#### validation 

* it's about test, e.g.  black box test, white box test, non-functional test
* it can find bugs which is not catched by verification 
* output is an actual product 

[V-model is an extension of waterfull model](https://www.professionalqa.com/v-model). The phases of testing are categorised as "Validation Phase" and that of development as "Verification Phase"


#### how simulation helps ?

* for validation to cover known and rara critical scenarios. 
* for verification to test whether the component function as expected


## model based to data driven 


| methodlogy | completeness | known | 0-error-gurantee | iterable | example | 
|--|--|--|--|--|--|--|
| model based | 1 | 1 | 1 | 0 | NASA |
| data driven  | 0 | 0 | 0 | 1 | Tesla Motor | 

with traditionally vehicle/airspace development, the system team first **clearly** define **all requirements** from different stakeholders and different departments, which may **take a long time**; then split to **use cases**, which is garanteed to be complete and all-known set, and **garantee zero-error**, the engineers just make sure each new development can meet each special verification. the general product design cycle is **3 ~ 5 years**, and once it release to market, there is little chance to upgrade, except back to dealer shops.

model based mindset need to control everything at the very beginning, to build a clear but validatable super complex system at very first, even it takes long long time. and the development stage can be a minor engineering process with a matured project driven management team. 

the goods of model based mindset is it strongly gurantee known requirements(including safety) is satisfied, while the drawback is it lose flexibility, slow response to new requirements, which means lose market at end.

to validate model based design ADS system, usually it highlights the full-cover or completeness of test cases, which usually can be pre-defined in semantic format(.xml) during system requirement stage. then using a validation system(e.g. a simulator) to parse the semantic test cases, and produce, run and analysis the test scenarios automatically.

in data driven ADS system, the system verification and validation strongly depends on **valid data**. 

1) data quantity and quality. as the data set can cover as many as plenty kinds of different scenarios, it's high qualitied； while if the data set have millions frames of single lane high way driving, it doesn't teach the (sub)system a lot really.

2) failure case data, which is most valueable during dev. usually the road test team record the whole data from sensor input to control output, as well as many intermediate outputs. what means a **failure case**, is the (sub)system (real) output doesn't correspond to expected (ideal) output, which is a clue saying something wrong or miss-handled of the current-version ADS system. of course, there are large mount of **normal case** data.

3) ground truth(G.T.) data, to tell the case as either normal or failure, needs an evaluation standard, namely **GT  data**. there are different ways to get GT data in RD stage and massive-producing stage. in RD stage, we can build a GT data collecting vehicle, which is expensive but highly-valued, of course it's better to automatically generate G.T. data, but manually check is almost a mandatory. a low-efficient but common way to get GT data by testing driver's eye. after data collection, usually there is off-line data processing with the event log by the driver. so the offline processing can label scenarios as **normal case** or **failure case**, usually we care more about **failure case**. in massive-producing stage, there is no GT data collecting hardware, but there is massive data source to get a very high-confidence classifer of failure or normal. 

4) sub-system verification, is another common usage of data, e.g. fusion module, AEB module, e.t.c. due to the limitation of existing sensor model and realistic level of SiL env, physical sensor raw data is more valued to verify the subsystem, which including more pratical sensor parameters, physical performance, physical vehicle limitation e.t.c, compared to synthetic sensor data from simulator, which is either ideal or statistically equal, or too costing to reach physical-level effect. 

5) AI model training, which consume huge data. during RD stage, is difficult to get that much of road data. so synthetic data is used a lot, but has to mixed a few portion of physical road data to gurantee no over-fit with semi-data. on the other hand, tha's a totally different story if someone can obtain data from massive-producing fleet, as [Telsa patented:SYSTEM and METHOD for obtaining training data](https://patentscope2.wipo.int/search/en/detail.jsf?docId=WO2020056331&tab=PCTBIBLIO): An example method includes receiving sensor and applying a neural network to the sensor data. A trigger classifier is applied to an intermediate result of the neural network to determine a classifier score for the sensor data. Based at least in part on the classifier score, a determination is made whether to transmit via a computer network at least a portion of the sensor data. Upon a positive determination, the sensor data is transmitted and used to generate training data. 

which is really an AI topic to learn from massive sensor data to understand a failure case. 

6) AI model validation, validation should depends on labeled valid dataset, e.g. G.T. data, or data verified from existing system, e.g. some team trust mobileyes output as G.T. data. 

7) (sub)system validation



## SiL sematic driven 

this mostly correspond to model based dev, there are a few issues about sematic driven SiL: 

1) build realistic-close sensor model, but how realistic it is compared to the real physical sensor ?  80% ?

2) virtual env from the SiL simulator, based on the virtual modeling ability. 

3)  1) + 2) -->  synthetic sensor raw data, which may have about 60%~80% realistic, compared to road test recording data

4) is there system bias of virtual/synthetic world ?  


during RD road test, we can record the failure scenario as semantic metadata(such as kind of OpenX/Python script), as well record the whole sensor & CAN data.

with semantic metadata, we import it to the SiL simulator, inside which create a virtual world of the senario. if the sensor configuration (include both intrinsic and extrinsic) in simulator is the same as the configurations in real test vehicles, and our sensor model in simulator can behave statistically equal to the real sensors, check [sensor statistical pars](), so it's almost a satistically realistic sensor model. 

sematic scenario description framework(SSDF) is a common way to generate/manage/use verification(functional and logic) scenarios libs and validation (concrete) scenarios libs. the benefits about SSDF is a natural extension of V-model, after define system requirements, and generate test cases based on each user case, namely sematic scenarios. 

but as we mentioned above, how precision the SiL performance and especially when comes to statiscally equal sensor model, namely, how to validate the accuracy loss or even reliability loss gap between synthetic and real envs, which is usually not considered well in sematic scenario based SiL. 

no doubt, synthetic data, or pure semantic scenario has its own benefits, namely fully labeled data, which can be used to as **ground truth** in virutal world or as input for AI training. again, we need to confirm how much realiabitliy these labeled data are, before we can 100% trust them.

Ideal ground truth/probabilistic sensor models are typically validated via software-in-the-loop (SIL) simulations. 

Phenomenological/physical sensor models are physics-based. They are based on the measurement principles of the sensor (i.e. camera uptakes, radar wave propagation) and play a role simulating phenomena such as haze, glare effects or precipitation. They can generate raw data streams, 3-D point clouds, or target lists.


## SiL data driven 






## sensor statistical pars 

* sensor accuracy model, kind of obeying **exponential distribution**, along side with the distance in x-y plane. further the sensor accuracy is speed、scenario etc depends. 

* sensor detection realiability(including false detection, missing detection), kind of obeying **normal distribution** , further can speicify obstacle detection realiability and lane detection realiability. 

* sensor type classification realiability, kind of **normal distribution**

* sensor object tracking realiability, kind of **normal distribution** 

* vendor nominal intrinsic, there is always a gap from vendor nominal intrinsic to the sensor real performance. e.g. max/min detection distance, FOV, angle/distance resolution ratio e.t.c. so we can use the test-verified sensor parameters as input for sensor model, rather than the vendor nominal parameters. 

as mentioned, there are lots of other factors to get a statistically equal sensor model, which can be considered iteration by iteration.

the idea above is a combination of statistical models, if there is a way to collect sensor data massively, a data-driven machine learning model should be better than the combination of statistical models. 


## data is the new oil

at the first stage, we see lots of public online data set, especially for perception AI training, from different companies e.g. Cognata, Argo AI, Cruise, Uber, Baidu Apollo, Waymo, Velodyne e.t.c. 

for a while, the roadmap to AI model/algorithms is reached by many teams, the real gap between a great company and a demo team, is gradually in build a massive data collection pipeline, rather than simply verify the algorithm works. the difference is between Tesla and the small AI team. 

this will be a big jump from traidional model based mindset to data-driven mindset, including data driven algorithm as well as data pipeline.

in China, the data center/cloud computing/5G is called **new infrastructure**, which will definitely accelerate the pocessing of building up the data pipline from massively fleet. 





## refere 

[difference of V vs V](https://www.guru99.com/verification-v-s-validation-in-a-software-testing.html)

[what are false alerts on a radar detector](https://radenso.com/blogs/radar-university/what-are-false-alerts-on-a-radar-detector)

[surfelGAN: synthesizing realistic sensor data for AD from DeepAI](https://deepai.org/publication/surfelgan-synthesizing-realistic-sensor-data-for-autonomous-driving)

[data injection test of AD through realistic simulation](https://www.microcontrollertips.com/data-injection-testing-autonomous-sensors-through-realistic-simulation/)

[avsimulation](https://www.avsimulation.com/)

[BMW: development of self driving cars](https://www.bmw.com/en/innovation/the-development-of-self-driving-cars.html)

[understand.AI. a dSPACE company](https://understand.ai/)

 [cybertruck talk](https://www.cybertrucktalk.com/threads/tesla-files-patent-for-sourcing-self-driving-training-data-from-its-vehicles.139/) 
 
 [tesla club](https://teslamotorsclub.com/tmc/threads/tesla-files-patent-for-sourcing-self-driving-training-data-from-its-fleet.189145/)






