
# rosbag tools in ADS

## background 

in ADS,  data fusion, sensor performance, L3+ perception, localization algorithms development relys a lot on physicall data collection, commonly in rosbag format with information/data about gps, rtk, camera, Lidar, radar e.t.c.

to build up the development process systemly is a critial thing, but also ignored by most ADS teams. for large OEMs, each section may have their own test vehicles, e.g. data fusion team,  sensor team e.t.c, but few of them take care data systematically, or build a solution to manage data. one reason is the engineers are lack of ability to give software tool feedbacks/requirements, so they still stay and survive with folders or Excel management, which is definitely not acceptable and scalable for massive product team. 

thanks for ROS open source community conributing a great rosbag database manage tool: [bag_database](http://wiki.ros.org/TheBagDatabase). with docker installation, this tool is really easy to configure. a few tips:

* web server IP port in Docker can be accessed from LAN by parameter `-p` during docker run.


## mount sbm drive

as mentioned, most already collected rosbag is stored in a share drive, one way is to mount these data.

```script 
sudo mount -t cifs //share_ip_address/ROS_data /home/david/repo/rosbag_manager/data  -o uid=david -o gid=david -o credentials=/home/david/repo/rosbag_manager/data/.pwd 


sudo umount -t cifs /home/david/repo/rosbag_manager/data

```


## Tomcat server configure

bag_database is hosted by Tomcat, the default port is 8080. For our services, which already host pgAdmin4 for map group; gitlab for team work; xml server for system engineering; for webviz. check the port is occupied or not:

```script 
	netstat -an | grep 8088 
```


so configure `/usr/loca/tomcat/conf/server.xml`:

```xml
	
<Service name="Catalina">
   <Connector port="your_special_port"
   ...
</Service>

```


## a few other tools

### ros_hadoop

[ros_hadoop](https://github.com/valtech/ros_hadoop) is a rosbag analysis tool based on hdfs data management. which is a more scalable platform for massive ADS data requirements. if there is massive ros bag process in need, ros_hadoop should be a great tool. there is a discussion in [ros wiki](https://discourse.ros.org/t/working-with-large-ros-bag-files-on-hadoop-and-spark/2314)


![image](https://github.com/valtech/ros_hadoop/blob/master/doc/images/concept.png)

![image](https://github.com/valtech/ros_hadoop/blob/master/doc/images/rosbag-analytics.png)


#### install hadoop

[apache hadoop download](https://hadoop.apache.org/releases.html)

[single alone install](https://poweruphosting.com/blog/install-hadoop-ubuntu/)


#### concept in hdfs 

* namenode 

daemon process, used to manage file system

* datanode 

used to data block store and query

* secondary namenode

used to backup


* [hdfs shell command](https://cloud.tencent.com/developer/article/1456436)

* [hdfs path URL](https://www.thomashenson.com/find-hdfs-path-url/)


#### hdfs-site.xml

	/usr/local/hadoop/etc/hadoop/hdfs-site.xml

[configure file](https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml)

* dfs.datanode.data.dir ->  local file system where to store data blocks on DataNodes 
* dfs.replicaiton ->  num of replicated datablocks for protecting data 
* dfs.namenode.https-address ->  location for NameNode URL 
* dfs.https.port -> 

#### copy local data into hdfs 


```script 

hdfs dfs -put /your/local/file/or/folder   [hdfs default data dir]

hdfs dfs -ls 

``` 


### mongodb_store 

[mongodb_store](https://github.com/strands-project/mongodb_store) is a tool to store and analysis ROS systems. also in [ros wiki](https://answers.ros.org/question/240699/ros_databases/)


### mongo_ros 

[mongo_ros](https://wiki.ros.org/mongo_ros) used to store ROS message n MongoDB, with C++ and Python clients.


### mongo-hadoop

[mongo-hadoop](https://github.com/mongodb/mongo-hadoop/) allows MongoDB to be used as an input source or output destination for Hadoop taskes. 


### ros_pandas 

[rosbag_pandas](https://nimbus.unl.edu/2014/11/using-rosbag_pandas-to-analyze-rosbag-files/)


### tabbles 

[tabbles](https://tabbles.net/) used to tag any rosbags or folders.


### hdfs_fdw

[hdfs for postSQL](https://github.com/EnterpriseDB/hdfs_fdw) 


## at the end 

talked with a friend from DiDi software team, most big Internet companies have their own software tool teams in house, which as I know so far, doesn't exist in any traditional OEMs. is there a need for tool team in OEMs? the common sense is at the early stage, there is no need to develop and maintain in-house tools, the commericial ones should be more efficient; as the department grows bigger and requires more user special development and commericial tools doesn't meet the needs any more, tool teams may come out. still most decided by the industry culture, OEM's needs is often pre-defined by big suppliers, so before OEMs are clear their software tool requirements/need, the suppliers already have the solutions there -- this situation is epecially true for Chinese OEMs, as their steps is behind Europen suppliers maybe 50 years.\

I am interested at the bussiness model of [autovia.ai](https://autovia.ai/), which focus on `distributed machine learning` and `sensor data analytics` in cloud with `petabyte of data`, with the following skills: 

*  large scale sensor data(rosbag) processing with Apache Spark

*  large scale sensro data(rosbag) training with TensorFlow

*  parallel processing with fast serialization between nodes and clusters 

*  hdmap generation tool in cloud 

*  metrics and visulization in web

*  loading data directly from hdfs, Amazon S3


all these functions will be a neccessary for a full-stack ADS team in future to development safety products, which I called " data infrastructure for ADS".


## refer

[MooreMike: ros analysis in Jupter](http://moore-mike.com/ros-analysis-part-2.html)

[mount smb share drive to ubuntu](https://askubuntu.com/questions/29535/how-do-i-access-a-mounted-windows-share-from-the-command-line)

[autovia.ai](https://autovia.ai/)








