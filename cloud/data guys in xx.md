### test reality 
currently, simualation driven test or data driven test is far beyond the reality of OEM teams. the benefit of simulation suppose to expose/find out issues at the early stage of the ADS system development, rather than after the system done.

so far, simulation doesn't really help a lot in the early stage. But when the ADS system is tested on highway, and failure scenario records, offline simulation helps to track the system variables as well as resimulation the failure scenarios.

### vehicle test  

rosbag is used to log videos during the test and helps to localize the time and position of an interested scenario/event. the corresponding vehicle pose info is recorded in `dlt`, which used in resimulation to track the variables.

during test, the failure scenario/event is manually written down by the testers, who record the fail event(such as sudden brake, can't lane change). and during offline replay, the tester will helps to correspond the event to the special scenario. 

### how to improve 

the benefits of a real human tester is, he/she can `feel` the driving performance of the test vehicle, but in simulation, how to catch these `human tester feelings` are missed. 

the problem is we don't have `criteria`/metrics/standard to describe these failure events. and since that, the power of simulation to drive ADS development is blocked.

one way to define the `criteria` is by vehicle testers, who summary the features; another way, maybe we can learn these `failure features` from the logging data, which further helps to define the `criteria` that satisfy sysem engineeing.

in both way, we will build the closed-loop data cycle to drive ADS development:

		ADS DEV -->  vehicle test(virtual and physical) --> Failure Analysis --> ADS DEV 


### the right way

if the team doesn't work efficently, while they are still working late, mostly it is a problem of management. 

first, the team has no clear direction about how to use data infrastructure for ADS development, of course the manager team don't know either. but we got the request from upper, that there will come a huge data, about 100T soon, so we'd better find out some solution to, at least store them.

so we actually designed the `data infrastructure` from bottom, far away from upper user requirements, due to the users(ADS developers, testers) has no idea about what tools or metholodgy will help, as well as no one has experince to estimate what is the right way to do things.

one issue is **blur bussiness roles and tech roles**. as traditional OEM, DREs or PMs are more profitable then mechanical engineers in general, so here people are more like talking in bussiness style, like leading a project with suppliers, getting collabaration with different component groups, which makes themselves feel great. even the developers has to fit in to touch with bussiness, rather than deep into the special development skills, which is very different from Internet, Finance companies. by default, there aer pure manage team and tech team, but sooner or later, they are almost in same bussiness function role, as the tech lead neither code or discuss tech details.

this phenomenon is dangerous, if the guy won't be a PM in OEM, then he/she almost lost his skills. 

the other issue is **lack estimate of work**. from top level to the develper. the lead team has no clear KPI for each section, nor how much work is there. so mostly they are passively driven by project timeline or external suppliers. without a clear estimation of each section or each worker, the lose of scientific and efficient performance assessment is no doubt. and also leading the project dead in middle. e.g. to build up the `data infrasturcture`, at least a 15 developer team to work about half year, but we have much less developers. if we still go on, in somewhere we will lost and can't move any more.



