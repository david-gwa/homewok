

## background 

why Waymo still can't release fully driveless cars on road; why vehicle startups, NIO is going to brankruptcy? one of the hidden reasons vehicle as a consumer product can't go to fast iteration as social media, mobility apps in Internet companies, is safety. 

vehicle development(VD) needs to satisfy safety requiements at first priority. so in VD,  the cutting edge tech/ new solutions usually doesn't make a difference, but the processes, how to handle safety requirements, system requirements, e.t.c are really the first thing in vehicle engineers' mind.

so now, deep learning AI in object detection is fairly matured, but it's not used common in vehicle camera products. and for these start ups, who say themselves as tech-driven doesn't survive well, because VD should be process driven. 

 the best managment/survive way for original equipment manufacture(OEM) companies is build up their process system. e.g. GM managemnet is about process, and Toyota agile management is about a more flexible process, too. no OEMs said their team is tech-driven. 
 
### what is SOTIF ? 

safety of the intended functionality(SOTIF): the absence of unreasonable risk due to hazards resulting from functional insufficiencies of the intended functionaliyt or by reasonably foreseeable misuse by persons.

SOTIF is a way to define `safey by design`, while still there are `unsafe post design`, which is beyond the standards can handle. 


### safety chanllenges in ADS

is conserative behaivor of AI unsafe ? YES. as Waymo cars driving in San Fransisco, it's more conservative than human drivers, which makes itself unsafe and surrounding vehicles unsafe. and the definiation of conservative or aggressive of driving behavior is further area depends, e.g. how human drivers drive in San Fransisco is different than drivers from Michigan, how AI handle this? 


how does AI satisfy VD requirements, and how to verify the AI really satisfy? there is no standard solution yet. since AI is black box, it may satisfy VD requirements in 99.9% situations, but failed in 0.1% case. 
 
an ADS solution works well in 99% scenarios is not an acceptable solution at all, which is really big chanllenge for most self driving full-stack solution start-ups. so Waymo and a few giants are working on test driven verification, which requires build up a very strong simulation team to power up safety test by simulation, which's even chanllenging for most traditional OEMs.

and definitely, there is no way to handle unstructured stochastic traffic environments,  


## classification of safety hazards 

* IS26262

* internal cyber security (ISO21434)

* functional insufficient & human misuse (IS02148)

* external infrastructura cyber security (traffic light system, jamming sensors signals)



## malfunction behaviors of EE 

Harzard Analysis & Risk Assignment 

		|
		|
		V
	
	ASIL B/C/D 		<--   sys requires 

	* func redundency 
	
	* system safety mechanism 
	
	* predictive safety mechanism 
	
this is a close-loop analysis, to satisfy `sys requirement` will get new situations, which lead to new system requirements 

	system requirements 
	
	  ^ 
	  |
	  |
	  V
	  
	SOTIF Analysis 

this is a double direction design, with any new requiremenst, there is a need to do SOTIF analysis, which may find out some potential bugs/problems in the design, then back to new system requirements.

in summary, the input to SOTIF analysis is system requirements, and output is new system requirements.


## functional insufficients 


* unsafe by design 

e.g. full pressure brake design, is not sufficient in scenarios, when there is rear following vehicle in full speed


## Tech limitations 

* safe known 

* unsafe known 

* safe unknown

* unsafe unknown 


SOTIF is to identify all unsafe cases and requies to make them safe, but not know how, but SOTIF can't predict unknown. 

back to why Waymo doesn't release their driveless vehicle yet, cause they don't have a way to prove their ADS system has zero unsafe unknown situations, and most possiblely the current ADS solution may be reached 80% functions of the final completed fully ADS solution, but that's even not the turning point for ADS system. 


## where to go? 

* rule based vs AI based 

as neither purely rule based nor purely AI based can achieve safety goals, so there are combined ways, but then there need a manager module to decide which should be weighted more in a special situation.

* a new undeterministic/unpredicted system explaination

reinforcement learning is actually a good way to train agents in unpredicted simulation environemnt, but even in simulation, it can't travel every case in the state space; then to use R.L to train vehicles in real traffic environment with random pedestrains, npcs, situations, which's impossible so far. 

* a new AI system 

current AI is still correlation analysis, while human does causal reasoning. 

 
## refer

[safety first for automated driving handover to PR]()

[ISO 26262 standard](https://www.iso.org/standard/70939.html)

[how to reach complete safety requirement refinement for autonomous vehicle](https://hal.archives-ouvertes.fr/hal-01190734/document)









