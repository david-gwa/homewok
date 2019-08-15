
## sample test framework 

1 identify concept ADS
2 identify attributes that define the operational design domain(ODD)
3 identify object and event detection and response(OEDR) capabilities
4 identify and assess faliure modes and failure mitigration strategies(FMFM)

### 7 generic categories

* L4 highly automated vehicle/transporation network company 
* L4 highway drive
* L4 low speed shuttle
* L4 valet parking
* L4 emergency takeover
* L3 highway
* L3 traffic jam



## driving system features 

focus on L3+

### ADS feature (SAE J3016)

a driving automation system's design-specific functionality at a specific level of driving automation within a particular Operational Design Domain.

#### design specific functionality 

* lateral vehicle motion control via steering
* longitudinal vehicle motion control via acceleration and deceleration
* monitoring the driving env via object and event detection, recognition, classification and response preparation
* object and event response execution
* maneuver planning
* enhancing conspicuity via lighting, signaling and gesturing


#### ODDs

#### FS/FO capability

fail-operational and fail-safe mechanisms. FO and FS mechanisms are used when an ADS fails, resulting in unintended functionality or behavior. Designing, testing, and validating these mechanisms ensures that an ADS can achieve a minimal risk operating condition that removes the vehicle and its occupants from harm’s way in the event of a failure.


### ADS tactical and operational maneuvers 

* parking
* maitain speed 
* car followin 
* lane centering
* lane switching/overtaking
* enhancing conspicuity, ADS vehicl blinkers, headlights, horn to comunicate with other vehicles
* obstacle avoidance
* low-speed merge
* high-speed merge
* right-of-way decisions
* follow driving laws
* navigate roundabouts
* navigate intersection, 
* navigate crosswalk
* navigate workzone
* N-Point turn
* U-turn
* route planning




## operational design domain

The ODD would include the following information at a minimum to define each ADS’s
capability limits/boundaries: Roadway types (interstate, local, etc.) on which the ADS is
intended to operate safely; Geographic area (city, mountain, desert, etc.); Speed range;
Environmental conditions in which the ADS will operate (weather, daytime/nighttime,
etc.); and other domain constraints (NHTSA, 2017a).


### ODD category descriptions

#### physical infrastructure

* roadway types
* roadway surfaces
* roadway edges
* roadway geometry

#### operational constraints

* speed limit
* traffic conditions
* objects(OEDR)
* signage
* roadway users 
* env conditions(visibility, sensro fidelity, vehicle maneuverability, communication systems)
* weather
* connectivity(v2v, v2i, remote manage/control)
* zones(geo-fencing, traffic management zone, school zones, work zones)


### ODD identification 


## object and event detection and response capabilities 

ODD analysis ->  driving scenario analysis -> OEDR analysis 

after correctly detection, there should be a stable control response, which includes:

* follow vehicle
* acc/decelerate
* stop
* yield
* change lane
* pass, shift into adjacent lane 
* turn
* shift within lane
* shift outside of lane
* move out of travel lane
* tansition to driver


## preliminary tests and evaluation methods 


### black box testing

the test involve position a large static obstacle along ADS's intended route and observing its ability to avoid a collision.  and only the resulting navigation outcomes is evaluated.



### white box testing
white-box testing will be identifying key interfaces for data measurement to support performance metrics

measuring the outputs ADS's perception or navigation algorithms to answer:

1) at what range did the ADS detect the obstacle ?
2) how quickly did ADS decide to react?
3) how stable was the control response ?



the test scenario framework can be viewed as an input or integrated component in the overall test scenario. each of the core scenario components cn be applied similarly for both black-box and white-box analysis.


test procedures includes:

* test subject and purpose 
* test personnel, facilities, equipment
* test scenario(inputs, initial conditions, execution, data measurement)

the principles to develop testing framework:

* test variables should e isolated 
* test environments should be characterized or controlled for test repeatability
* test metrics should not contain inherent thresholds 
* low-level test should help create boundary conditions for high-level integrated system tests
* parameterization of testing variables and conditions should forcus on a "reasonable worst case"




### test scenarios 

the core aspects of a common ADS test scenario:


* tactial maneuver behaviors
* ODD elements
* OEDR capabilities
* Failure mode behaviors


|scenario elements   | example   |
|---|---|
| tactical maeneuver behaviors | perform lane change |
| ODD elements |   straigh  flat road |
|              |   Arterial roadway type | 
|              |  72kph speed limit|
|              |  clear, dry weather |
|              |  night time|
| OEDR behaviors|   detect and respond to frontal/side/rear adjacent vehicles |
| failure mode behaviors | N/A |


a test case example:

These scenarios show a hypothetical progression of testing, starting with a simple case with no vehicles in the adjacent lane and iteratively getting more complex to a situation where the vehicles in the adjacent lane are spaced such that there is insufficient room for the ADS to safely merge.



### test chanllenges 

#### chanllenges associated with ADS technology 

* probabilistic and non-deterministic algorithms, e.g.  heuristics or probability to provide a best guess

* machine learning algorithms,  e.g. CNN in image detection

* digital mapping needs, 

* regression testing,  how to test Over-The-Air ?  


#### chanllenges associated with test execution

* testing completeness,  the number of tests or miles driven required to achieve statistical significance to claim safe operation could be staggering 


* testing execution controllability, 

* testing scalability, to achieve significant coverage of the variety and combination of conceivable test conditions

* unknown/unclear constraints/operating conditions,  corner cases in real-world, e.g. missing lane markers

* degraded testing, testing against ideal conditions vs a reasonable worst case scenarios 

* infrastucture considerations 

* laws and regulations 

* assumptions, e.g. other vehicles will obey rules of road 



## Fail operational and fail safe mechanisms 

when system doesn't function as intended, FO/FS will take over.


MRC, A condition to which a user or an ADS may bring a vehicle after performing the DDT
fallback in order to reduce the risk of a crash when a given trip cannot or should not be
completed.



### FMEA design

* identify potential failure modes 
* identify potential causes and effects of those failure modes 
* prioritize the failure modes based upon risk
* identify an appropriate corrective action or mitigation strategy 

|Behavior Failure   |  Effects |
|---|---|
|Fail to maintain lane |  Impact adjacent vehicle or infrastructure | 
|Fail to maintain safe following distance | Impact lead vehicle |
| Fail to detect and respond to maneuvers by others | Impact lead or adjacent vehicles |
| Fail to detect relevant obstacles in or near lane | Impact obstacles |
| Fail to identify ODD/OEDR boundary | Operate outside of ODD/OEDR capabilities |




### failure mitigration strategies


### fail-safe mechanisms

### fail operational mechanisms























