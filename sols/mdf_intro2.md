
#### sensor raw data vs sensor physical data 

tips, `sensor physical data` here means the sensor raw data input to MCU, and go through `sensor_Step()`, with `CR_OBJ_BUS` kinds of data. 

both are collected and stored in mf4, we use `sensor physical data` previously, as we only care about the input to the high level application, e.g. AEB modules. 

as we go through embedded integration code and with embedded middleware, there is the ability to handle raw sensor data with `sensor_Step()`. 

inside `sensor_Step()`, it's basically transfer sensor raw data into global structures, which are used as the input for upper adas functions 

to use these global structures, the middleware offer Iread/Iwrite APIs, which are called inside `application_Steps()`, such as `tos_Step()`, so basically these global structures are hiddend from `appication_Steps()`, but only these getter/setter APIs.

NOW if we continue with `sensor physical data`, we need mock/modify `sensor_Step()`, but for `application_Steps()`, we continue to use these getter/setter APIs defined in middleware. 


the other output from `sensor_Steps()` is `canfd message`



#### mdf intro

[vector mdf struct](https://www.asam.net/standards/detail/mdf/wiki/)



### raw vs physical(human readable) 


raw bus data -->  human readable aka "phyiscal" or "scaled" values ,  through a conversion rules:  DBC file

With a DBC, you can use asammdf to convert your raw data. The resulting MDF file contains a Data Group for each CAN ID and a Channel for each message signal.


```python
classasammdf.blocks.v2_v3_blocks.Channel(**kwargs)
```

* ChannelConversion 

* load_metadata


### channel conversion


[mdf wiki](https://www.asam.net/standards/detail/mdf/wiki/)

##### conversion rules

the input of a conversion rules either is a numeric value or a string. Its result again either is a numeric value (by definition a 64 bit floating point value) or a string (by design always UTF-8 encoded due to the usage of TX blocks in tabular look-up conversions).
