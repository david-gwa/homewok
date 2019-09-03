

## background of Vehicle Dynamics(VD)

the forward flow of VD:  driver control steering input, go to motor engine, output torque, which then gointo gearbox and transfer as powertrain torque, which then apply to wheel pairs. 

the backward flow of VD: the ground force acted on wheel pairs, transfer to torque, which then acted on the vehicle body, which influence the driver control.




## how Wheel Collider component works to get a car working in Unity ? 

[refer](http://www.theappguruz.com/blog/unity-wheel-collider-for-motor-vehicle-tutorial-2018)

![image](http://www.theappguruz.com/app/uploads/2018/06/car-as-per-unity.png)


any vehicle in Unity is a combination of:  4 wheels colliders and 1 car collider.


* wheel damping rate 

* force app point distance 

* suspension spring (K, R)

* Forward Friction (slip)

* Sideways Friction (slip)


![physical of wheel](http://www.theappguruz.com/app/uploads/2018/06/physics-of-wheel-collider.png)


* Sprung mass (not weight) is used to apply individual force on each wheel.

* Suspension Distance is the distance between max droop and max compression. 

    Suspension Force(F) = (sprungMass * g ) +( jounce * stiffness) - (damper * jounceSpeed)

jounce 		offset of the wheel relative to the rest pose.
stiffness 	that means physics friction. (setting this to 0 means no friction change this runtime to simulate in various ground material).
damper 		damping value applied to the wheel
jounceSpeed 	wheel moved with suspension travel direction.




AxleInfo 
{
  WheelCollider  left ;
  WheelCollider right; 
  GameObject leftVisual ;
  GameObject  rightVisual ;
  bool motor ;    #enable movement of this wheel pair
  bool steering ; # enable rotation of this wheel pair 
  float brakeBias = 0.5f; 
}


### WheelCollider

[unity doc](https://docs.unity3d.com/Manual/class-WheelCollider.html)

[unity official](https://docs.unity3d.com/ScriptReference/WheelCollider.html)

[unity tutorial](https://docs.unity3d.com/Manual/WheelColliderTutorial.html)

1) core parameters 

* wheel damping rate 

* suspension distance 

* Force apply point distance (where ground force act on wheel) 

* suspension spring 

* forward/sideways friction


2) process 
vehicle controlled by  `motorTorque`,  `brakeTorque`, `steerAngle` ;  the wheel collider computes the firction separately from the Unity physics engine, using a slip-based friction model

3) visualization

the `WheelCollider` GameObject is always fixed relative to the vehicle body, usually need to setup another visual GameObject to represent turn and roll.


[implementation from lg-sim](https://github.com/lgsvl/simulator/blob/master/Assets/Scripts/Controllers/VehicleController.cs)

```c#
void ApplyLocalPositionToVisuals(WheelCollider collider, GameObject visual)
    {
        Transform visualWheel = visual.transform;

        Vector3 position;
        Quaternion rotation;
        collider.GetWorldPose(out position, out rotation);

        visualWheel.transform.position = position;
        visualWheel.transform.rotation = rotation;
    }
```

4) WheelCollider.ConfigureVehicleSubsteps

```shell
public void ConfigureVehicleSubsteps(float speedThreshold, int stepsBelowThreshold, int stepsAboveThreshold); 

```
Every time a fixed update happens, the vehicle simulation splits this fixed delta time into smaller sub-steps and calculates suspension and tire forces per each smaller delta. Then, it would sum up all resulting forces and torques, integrate them, and apply to the vehicle's body.

5) WheelCollider.GetGroundHit
return the ground collision data for the wheel

6)  WheelHit 
[unity official](https://docs.unity3d.com/ScriptReference/WheelHit.html)

* forwardSlip(slip angle),   tire slip in the rolling direction, which is used in calculating torque
* sidewaySlip 


### wheel friction curve
for wheels' forward(rolling) direction and sideways direction, first need to determine how much the tire is slipping, which is based on speed difference between the tire's rubber and the road,
then this slip is used to find out the tire force exerted on the contact point 

the wheel friction curve taks a measure of tire slip as an Input and give a force as output.  

The property of real tires is that for low slip they can exert high forces, since the rubber compensates for the slip by stretching. Later when the slip gets really high, the forces are reduced as the tire starts to slide or spin

1) AnimationCurve 
[unity official](https://docs.unity3d.com/ScriptReference/AnimationCurve.html)

store a collection of Keyframes that can be evaluated over time  

2) slider & toggle 
slider bar


###  VehicleController parameters:

```shell

currentGear 
currentRPM
currentSpeed 
currentTorque
currentInput 
steerInput 

```

1) math interpolate function used
	Mathf.Lerp(a, b, t)

a -> the start value 
b -> the end value 
t -> the interpolation value between start and end 


2) fixedupdate for VD 

```shell
rigidBody.AddForce(air drag)
rigidBody.AddForce(down force)
rigidBody.AddForceAtPosition(tire drag, position)
# calc current gear ratio
# calc engine RPM, interpolate by current RPM and wheelRPM
# convert inpus to torques 
steer = maxSteeringAngle * steerInput 
currentTorque = rpmCurve.Evaluate(currentRPM / maxRPM) * gearRatio * finalDriveRatio * tractionControlAdjustedMaxTorque;
ApplyTorque()
TractionControl()
currentSpeed = rb.velocity.magnitude 
deltaDistance = wheelsRPM / 60.0f * (axles[1].left.radius * 2.0f * Mathf.PI) * Time.fixedDeltaTime;
deltaConsumption = ;
consumptionDistance = deltaConsumption / deltaDistance ; 
consumptionTime = deltaConsumption / fixedDeltaTime ;
fuelLevel -= deltaConsumption ;
engineTemperatureK = ;
turnSignalTriggerThreshold = 0.2
turnSignalOffThreshold = 0.1

private  AutoSteer()
            rb.velocity = Quaternion.AngleAxis(yawRate * autoSteerAmount, Vector3.up) * rb.velocity;

private ApplyTorque()
{
	       float torquePerWheel = ignitionStatus == IgnitionStatus.On ? accellInput * (currentTorque / numberOfDrivingWheels) : 0f;
	 if(acc)
		foreach (axle in axles): 	    
			axle.left.motorTorque =  torquePerWheel ;
		    	axle.left.brakeTorque = 0f;
	else
}

private TractionControl()
{
	AdjustTractionControlTorque(axle.hitLeft.forwardSlip)
}
			
private AdjustTractionControlTorque(forwardSlip)
{
   if(forwardSlip > SlipLimit)
	tractionMaxTorque -= 10 
   else 
        tractionMaxTorque += 10 
}

# the `tractionMaxTorque` will be used to update currentTorque
	
```
















