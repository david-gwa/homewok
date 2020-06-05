

## what about system engineering design

the following idea is coming from the expert of system engineering. 

originally, system engineering or model based design sounds come from aerospace, defense department. the feature of these products: 

1) they are the most complex system

2) they are sponsored by the goverment
  
3) they are unique and no competitors

which means they don't need worry about money and time, so to gurantee the product finally works, they can design from top to down in a long time. 


the degrade order of requirements level comes as:

areospace, defense product >>  vehicle level product >>  industry level product >> customer level product

 
usually the techs used in the top level is gradually degrading into the next lower level in years. e.g. GPS, Internet, autonomous e.t.c. at the same time, the metholodies from top level go to lower level as well. 

I suppose that's why system engineeering design comes to vehicle industry. however, does it really work in this competitional industry?  I got the first experince when running scenaio testes in simulation SIL. as the system engineering team define the test cases/scenarios, e.g. 400 test scenarios; on the other hand, the vehicle test team does the road test a few times every week.the result is, most time the 400 test scenarios never catch a system failure; but most road test failure scenario does can be repeated in the simulation env.

system engineering based design doesn't fit well. there are a lot reasons. at first, traditionally the design lifetime of a new vehicle model is about 3~5 years, and startup EV companies recently has even shorter design life cycle, about 1~2 years. so a top-down design at the early time, to cover every aspect of a new model, does almost not make sense. in the V development model, most fresh engineers thought the top-down design is done once for all, the reality is most early stage system engineering desgin need be reconstructured. 


secondly, system engineering design usually is abstract and high beyond and except engineering considerations, as the system engineers mostly doesn't have engineering experience in most sections of the sysetem. which results in the system engineering based requirements are not testable, can't measure during section implementation.

there are a few suggestions to set a workable system engineering process: 

the system engineering team should sit by the develop teams and test teams, they should have a lot of communication, and balance the high-level requirements and also testable, measurable, implementable requirements. basically, system engineering design should have product/component developers as input.

both the system engineers and developers should understand the whole V model, including system requirements, component requirements are iteratable.

focus on the special requirement, and not always start from the top, each special requirement is like a point, and all these existing points(already finished requirements) will merged to the whole picture finally.

take an example, during the road test, there will come a new requirement to have a HMI visulization,  then focus on this HMI requirement, cause this requirements may not exist in the top down design. but it is the actual need.

   

## what about system test and verification 
  
as most OEMs have said they will massive product L3 ADS around 2022, it is the time to jump into the ADS system test and verification. just knew that Nvidia has the full-stack hardware lines: the AI chips in car(e.g. Xavier), the AI training workstation(e.g. DGX), and the ADS system verifcation platform(e.g. Constallation box).


#### data needs 
the ADS development depends a lot on data infrastructure:

	data collect --> data storage --> data analysis

there are many small pieces as well, e.g. data cleaning, labeling, training, mining, visulization e.t.c
  
from different dev stage or teams, there are different focus. 

* road test/sensor team, they need a lot of online vehicle status/sensor data check, data logging, visulization(dev HMI), as well as offline data analysis and storage 

* perception team, need a lot of raw image/radar data, used to train, mine, as well as to query and store.

* planning/control team, need high quality data to test algorithms as well as a good structured in-car computer.

* HMI team, are focusing on friendly data display 

* fleet operation team, need think about how to transfer data in cloud, vehicle, OEM data centers e.t.c.

 
sooner or later, data pipepline built up is a have to choice.
 


#### data collection vendors
road test data collection equipment used in ADS development, is actually not a very big market, compared to in-var computers. but still there are a few vendors already. 

* the top chip OEMs, e.g.  Nvidia, Intel has these products.
* chip poxy, e.g.  Inspire 
* traditional vehicle test vendors, e.g. Dspace, Vector, Prescan
* startups, e.g. horizon 



#### Nvidia constellation

ADS system test usually includes simulation test and road test. and the road test is also called vehicle-in-loop, which is highly expensive and not easy to repeat; then is hardware-in-loop(HIL) test, basically including only the domain controller/ECU in test loop; finally is the  is software-in-loop(SIL) test, which is most controllable but also not that reliable.

in practical, it's not easy to build up a closed-loop verification(CI/CD) process from SIL to HIL to road test. and once CI/CD is setted up, the whole team can be turned into data/simulation/test driven.  

the difficult and hidden part is the supporting toolchain development. Most vehicle test vendors have their special full-stack solution toolchains, but most of them are too eco-customized, it's really difficult for ADS team, specially OEMs, to follow a speical vendor solution.

another reason, test vehicles include components from different vendors, e.g. camera from sony, radar from bosch, Lidar from a Chinese startup, logging equipment from dSpace, and ECUs from Conti. which makes it difficult to fit this mixed system into a Vector verification platform. 


Nvidia Constallation is trying to meet the gap from SIL, HIL to road test. as it can suppport most customized ECUs.

* from road test to HIL, it use the exactly same chip. 

* for road test resimulation,  Nvidia offer a sim env, and the road test log can feed in directly

the ability to do resimulation of road test is a big step, the input is directly scanned images/cloud points, even lgsvl, Carla has no such direct support. but resimulation is really useful for CI/CD. Nvidia constallation as said, is the solution from captured data to KPIs.

another big thing is about their high-level scenario description language(HLSDL), which I think is more abstract than OpenScenario. the HLSDL engine use hyper-parameters, SOTIF embedded scenario idea, and optimized scenario generator, which should be massive, random as well as KPI significantly, it should be a good scenario engine if it has these features. 

## Bosch VMS

vehicle management system(VMS) is cloud nature framework from Bosch, which is used to meet the similar requirements as Nvidia's solution, to bring the closed-loop(CI/CD) from road test data collection, data anlaysis to fleet management. they have a few applications based on VMS:

*  fleet batteries management(FBM)

for single vehicle's diaglostic, prediction; and for the EV market, FBM can be used as certification for second-hand EV dealers

* road coefficient system(RCS)

Bosch has both in-vehicle data collection box and cloud server, RCS will be taken as additional sensor for ADS in prodcut

* VMS in itself

Bosch would like to think VMS as the PLM for ADS, from design, test, to deployment. and it shoul be easy to integrate many dev tools, e.g. labeling, simulation e.t.c



## what about safety 

as mentioned previously, 80% of Tesla FSD is to handle AI computing, Nvidia Xavier has about 50% GPU; Mobileye has very limited support for AI. all right, Tesla is most AI aggressive, then Nvidia, then Mobileye is most conserved. which make OEMs take Mobileye solution as more safety, but AI does better performance in perception, so how to balance these two ways? 

I realized the greats of Mobileye's new concept: `responsibility sensitive safety`(RSS), RSS can be used as the ADS safety boundary, but inside either AI or CV make the house power. a lot of AI research on mixed traditional algorithms with AI algorithms, RSS sounds the good solution. would be nice to build a general `RSS Mixing AI`(RMA) framework.

 









