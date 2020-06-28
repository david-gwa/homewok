
## why ViL ?

ViL is the last two step in evaluation and verification before releasing a new vehicle product. as ViL is close to the real car system. the benefits is to offer the real vehicle dynamic, which means the real vehicle respond and delay e.t.c. 

for functions/features development, ViL also helps to calibrate the boundary of some system parameters, which saves a lot of energy of calibration engineers, as they don't need to the test field and prepare and run the real vehicles day by day.

## how ViL works ?

the logic of ViL is to integrate the real vehicle (dynamic) into a virtual test environment(VTE):

* forward: the real vehicle send vehicle dynamic data(vehicle position, heading, speed e.t.c) to VTE;

* backward: VTE split out env information to the real vehicle, which is handled by SoC in vehicle. 


 so first need prepare a VTE, and the VTE should have the ability to support external vehicle dynamic(VD) plugin, which is a common feature of VTE, e.g. [lgsvl full model interface](https://www.lgsvlsimulator.com/docs/ego-vehicle-dynamics/)

secondly, VTE has the ability to export sensor data, which includes exporting data type and exporting data protocol. the common solution is `rosbag` through `ros` communication.

## ViL in reality 

the ideal way of plugin real vehicle dynamic into VTE is throuh full-model-interface(FMI), which is especially true for SiL. 

for forward data, vehicle dynamic data here only requies real vehicle position information, which can be obtained in a few ways. from vehicle CAN bus, or from RTK sensor, or from upper application layer, e.g. vehicle status module. but most VTE normally support ros message parsing, rather than CAN message parsing. so additionaly need to define a CAN-ROS message adapter. 

for backward data, most VTE(e.g. LG) does have some kind of message channels, e.g. sensor ros topices, which can be used to publish the virtual environment information(sensor data). or VTE may have well-supported sensor message exporter.

## limitations 

the ViL solution above is an useable and very customized solution, so the extenable ability and data/model precision is limited. 



 

 



