
## a memory efficient reader 


to read channels from mdf4, the first idea:

```py
def multi_init_read(channle_namelist)
```

the `channel_namelist` is customized defined, which is related to the customized output strucuture, which we call `custom_group`. so the memory allocation is a dictionary nest dictionary:

```py
cacheMap{"custom_group_name": {"channel_1": instance1, "channel_2": instance2, ...} }
```

to fill in this nest dict data strucutre, the mdf4 file handler need jump among different memory sections. 


an obviously optimized way is to use the built-in `select()` API, which should have a better memory reading performance than reading `channel_namelist` rawlly.


and further, we can use `get_group()` and the `group names` in mdf4 files to do reading, rather than custom the group_names, which has two benefits: 1) better memory reading performance, as the mdf4 data is organized by its `group names` and channels; 2) `group name` is additionaly flags to read channels, especially in case where the different groups have same channel names.

 
```py
groupDfCacheMap[group_name] = reader.get_group(groupIdx)
```


## asammdf APIs


#### select()

an [example](https://github.com/danielhrisca/asammdf/issues/187):

1. read the file 
2. find which signals are available
3. create a df to contain all the signals 
4. store data frame as pickle file

``py
signal_list = []
for items in ROI :
	y = mdf.whereis(df, items)
	if y:
		signal_list.append(items)

df = mdf.select(channels=signal_list, dataframe=True)
```

#### to_dataframe()

an [example](https://github.com/danielhrisca/asammdf/issues/187):

```py
signal_list = []
for items in ROS:
	y = mdf.whereis(df, items)
	if y  :
		signal_list.append(items)

df = mdf.to_dataframe(channel=fl, raster=1)

```

the performance can check [here](https://github.com/danielhrisca/asammdf/issues/187#issuecomment-492814480). it's about **1.46G mdf4 data, taking 2mins**

MDF is designed to handle signals with different sampling rates. Inside a channel group all the channels have the same timebase.


#### export()

an [sample](https://github.com/danielhrisca/asammdf/issues/152)


```py
csv = mdf.export(fmt="csv")
```
generate a new csv file for each data group (<MDFNAME>_DataGroup_<cntr>.csv)

#### get_group()





#### resample()


resample all channels using the given raster, returned a new MDF with resampled channels.

an [sample](https://github.com/danielhrisca/asammdf/issues/173)


`resample` can take arguments as channel_name, or custom arrays or a float, depending on asammdf lib version.



#### iter_get()

an [sample](https://github.com/danielhrisca/asammdf/issues/244): 

```python
import numpy as np
intVal = 0
for file in FileListManual:
    with MDF(file) as mdf:
        for ch_part in mdf.iter_get(IntChannel):
            intVal += np.sum(ch_part.samples[1:] * np.diff(ch_part.timestamps))
```


#### master channel

an [sample](https://github.com/danielhrisca/asammdf/issues/301):

```py
for i, gp in enumerate(mdf.groups):
    master = mdf.masters_db[i]
    master_channel = gp.channels[master]
    print(i, gp.channel_group.metadata(), master_channel)
```

* `group.metadata()` : 

```yml
id                         : b'##CG'
reserved0                  : 0
block_len                  : 104
links_nr                   : 6
next_cg_addr               : 0x0
first_ch_addr              : 0x342ae8
acq_name_addr              : 0x342b88
acq_source_addr            : 0x342d30
first_sample_reduction_addr: 0x0
comment_addr               : 0x342bb8
record_id                  : 1
cycles_nr                  : 2081
flags                      : 0
path_separator             : 0 (= <undefined>)
reserved1                  : 0
samples_byte_nr            : 48
invalidation_bytes_nr      : 0
```


* `master_channel` :

```yml
<Channel (name: t, unit: , 
          comment: <CNcomment>
		<TX>OBJ_FUSION_TYPE</TX>
	        <raster>0.01</raster>
	 </CNcomment>, 

          address: 0x342ae8,
	  source: None,
          fields: address:3418856, attachment:None, attachment_nr:0, bit_count:64, bit_offset:0, block_len:160, byte_offset:0, channel_type:2, 
          comment:<CNcomment>
 		     <TX>OBJ_FUSION_TYPE</TX><raster>0.01</raster>
	          </CNcomment>, 
```


#### raster 


an sample: [fill an array with the lit of all Signal name and sample rate](https://github.com/danielhrisca/asammdf/issues/321)

```py
    def get_group_sampling_rates(self):
        sampling_rates = dict()
        for i, group in enumerate(self.reader.groups):
            master = self.reader.get_master(i)
            gname = group['channel_group'].acq_name
            if len(master) > 1:
                rate = np.mean(np.diff(master))
            else:
                rate = 0
            sampling_rates[gname] = rate
        return sampling_rates

```

#### get_start_end_time()

[sample](https://github.com/danielhrisca/asammdf/issues/331)

```py

def get_start_end_time(self):
        t_min = []
        t_max = []  
        for group_index in self.reader.virtual_groups:
            group = self.reader.groups[group_index]
            cycles_nr = group.channel_group.cycles_nr
            if cycles_nr:
                master_min = self.reader.get_master(group_index, record_offset=0, record_count=1,)
                if len(master_min):
                    t_min.append(master_min[0])
                    master_max = self.reader.get_master(group_index, record_offset=cycles_nr - 1, record_count=1,)
                    if len(master_max):
                        t_max.append(master_max[0])

        if t_min:
            t_min_short = np.amin(t_min)
            t_min_long = np.amax(t_min)
            t_max_short = np.amin(t_max)
            t_max_long = np.amax(t_max)

        print("t_min_short", t_min_short)
        print("t_min_long", t_min_long)
        print("t_max_short", t_max_short)
        print("t_max_long", t_max_long)

        return (t_min_long, t_max_short)

```





## pandas.DataFrame

* basic operation on DataFrame

```py
for idx, row in df_instance.iterrows():
	print("idx from df_instance", idx)
	print("row val from df_instance", row)

df.empty
df.loc[]  #parameter with column_name and index_name
df.iloc[]  #parameters with index location (1,2,..)
df.col_name.to_list()[0]
df[col_name].to_list()[0]
df[col_name].values[0]

```


* iterate over DataFrame

```py
tts = len(freader.dfCache['group_name'])
df_iter  = freader.reader.dfCache['group_name'].iterrows()
for ts in range(tts):
	cur_df_slice = next(df_iter)[1]
```




## refere

[fill an array with the lit of all Signal name and sample rate](https://github.com/danielhrisca/asammdf/issues/321)

[asammdf vs mdfreader performance](https://github.com/danielhrisca/asammdf/issues/137#issuecomment-471957899)

[stackoverflow:  pandas DataFrame performance](https://stackoverflow.com/questions/22084338/pandas-dataframe-performance)



















