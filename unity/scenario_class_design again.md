
## utils for scenarios 

```python 
 get_distance_along_route() ?  -> 

 get_crossing_point() ?  ->  crossing point location in front of ego 

 get_geomeric_linear_intersection() -->  two actors' intersection points

 get_location_in_distance()

 get_location_in_distance_from_wp() 

 generate_target_waypoint_list() # follow waypoints to a junction and choose a path based on turn input 

 detect_lane_obstalce() 

```


## integration obstacle manager   

 get obstacle location once 


## static obstacles in front of current lane scenario
### behavior definition
spawn obstacle at transform.position
ego finally stopped distance to obstacle at least 5m


### test criteria 
ego collision criteria 


## static obstacles in front of current target scenario
### behavior definition
spawn obstacle at transform.position
ego finally stopped distance to obstacle at least 5m


### test criteria 
ego collision criteria 
ego lane-change criteria 


## static obstacles in neighbor lane scenario
### behavior definition
spawn obstacle at transform.position

### test criteria 
ego collision criteria 



## npc slow-speed in front of ego scenario
### behavior definition
spawn npc in front of ego 
npc drive to next intersection:
	npc follow closest lane with a low speed 
	npc stop inside of intersection(5m)
 
### test criteria 
ego/npc non-collision
ego/npc max-speed 


## npc abnormal-speed in front of ego scenario
### behavior definition
spawn npc in front of ego 
npc drive to next intersection:
	npc follow closest lane with a normal speed
	npc decellerate to 0 in 2s
	npc follow closet lane with a normal speed again
	npc stop inside of intersection(5m)
 
### test criteria 
ego/npc non-collision
ego/npc max-speed 


## npc cut-in current lane 
### behavior definition
spawn npc in neighbor lane 
npc drive to next intersection:
	npc follow closest lane with a normal speed in current lane
	npc lane change 
	npc follow closet lane with a normal speed in the new lane 
	npc stop inside of intersection(5m)
 
### test criteria 
ego/npc non-collision
ego/npc max-speed 


## npc cut-off current lane 
### behavior definition
spawn npc in front of current lane 
npc drive to next intersection:
	npc follow closest lane with a normal speed in current lane
	npc lane change to neighbor lane 
	npc follow closet lane with a normal speed in the neighbor lane 
	npc stop inside of intersection(5m)
 
### test criteria 
ego/npc non-collision
ego/npc max-speed 



## traffic jam 
### behavior definition
spawn 6 npcs in front of ego, in all lanes 
foreach npc in npcs:
	npc stand still
 
### test criteria 
ego/npc non-collision
ego/npc max-speed 







