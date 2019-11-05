
## udpHandler 

* IPEndPoint()

* Socket class

* Socket.ReceiveFrom()

* System.Runtime.InteropServices

* Thread or Coroutine 

* StructueToPtr 


## udp matlab communicate with lg-sim


## vehicle dynamic 



### concepts 


* motor torque 

* brake torque 

* steering angle 

* idle RPM 

* max RPM 

* gearbox ratio

* gear change shift delay 

* gear shift to complete 

* throttle 

* air drag coeff

* air down force coeff 

* tire drag coeff 

* wheel damping 

* autosteer 

* traction control 

* wheel collider

`traction control limits torque based on wheel slip`,  `wheel damping`, 



axles[0] front wheel pair <left, right>

axles[1] rear  wheel pair <left, right>


* unity API WheelCollider.ConfigureVehicleSubsteps

```shell
public void ConfigureVehicleSubsteps(float speedThreshold, int stepsBelowThreshold, int stepsAboveThreshold); 

```
Every time a fixed update happens, the vehicle simulation splits this fixed delta time into smaller sub-steps and calculates suspension and tire forces per each smaller delta. Then, it would sum up all resulting forces and torques, integrate them, and apply to the vehicle's body.




* unity API AxleInfo 









