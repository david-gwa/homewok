

## background 

hadoop is the base for most data center


## prepare jdk and hadoop in single node 


#### jdk in ubuntu

Java sounds like a Windows langage, there are a few apps requied Java in Ubuntu, e.g. osm browser e.t.c., but  I can't tell the difference between `jdk` and `jre`, or  openjdk vs Oracle.  `jdk` is a dev toolkit, which includes `jre` and beyond. so when it's always better to set `JAVA_HOME` to `jdk` folder. 

there are many different version of jdk, e.g. 8, 9, 11, 13 e.t.c.  here is used `jdk-11`, which can be download from Oracle website, there are two zip files, the `src` and the other. the pre-compiled zip is enough to Hadoop in Ubuntu.

``` 
tar xzvf  jdk-11.zip  
cp -r jdk-11  /usr/local/jdk-11 
cd /usr/local
ln -s jdk-11 jdk
``` 

append `JAVA_HOME=/usr/local/jdk && PATH=$PATH:$JAVA_HOME/bin` to `~/.bashrc`, and can run test `java -version`.

what need to be careful here, as the current login user may be not fitted for multi-nodes cluster env, so it's better to create the `hadoop group` and `hduser`, and use `hduse` as the login user in following steps.


#### create hadoop user

```
sudo addgroup  hadoop
sudo adduser --ingroup hadoop  hduser 
sudo - hduser #login as hduser
```

the other thing about `hduser`, is not in `sudo` group, which can be added by:

curren login user is `hduser`:

```
groups  # hadoop
su -  # but password doesn't correct
#login from the default user terminal
sudo -i  
usermod -aG sudo hduser
#backto hduser terminal
groups hduser  # :  hadoop  sudo 
exit 
su - hduser  #re-login as hduser 
``` 

#### install and configure hadoop 

hadoop installation at Ubuntu is similar to Java, which has src.zip and pre-build.zip, where I directly download the `pre-build.zip`.

another thing need take care is the version of hadoop. since `hadoop 2.x` has no `--daemon` option, which will leads error when master node is with `hadoop 3.x`.

```
tar xzvf  hadoop-3.2.1.zip  
cp -r hadoop-3.2.1 /usr/local/hadoop-3.2.1
cd /usr/local
ln -s hadoop-3.2.1 hadoop
```

add `HADOOP_HOME=/usr/local/hadoop` and `PATH=$PATH:$HADOOP_HOME/bin` to `~/.bashrc`. test with `hadoop version`

[hadoop configure is find here](https://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-multi-node-cluster/)


there is another issue with `JAVA_HOME not found`, which I modify the `JAVA_HOME` variable in `$HADOOP_HOME/etc/hadoop/hadoop_env.sh` 


#### passwordless access among nodes 

* generate SSH key pair

```
on maste node:
ssh-keygen -t rsa -b 4096 -C "master"
on worker node:
ssh-keygen -t rsa -b 4096 -C "worker"
```

the following two steps need do on both machines, so that the local machine can ssh access both to itself and to the remote.


* enable SSH access to local machine

	ssh-copy-id hduser@192.168.0.10


* copy public key to the remote node

	ssh-copy-id hduser@192.168.0.13


[tips](https://linuxize.com/post/how-to-setup-passwordless-ssh-login/), if changed the default `id_rsa` name to sth else, doesn't work. after the changes above, will generates a `known_hosts` at local machine, and an `authorized_keys`, which is the public key of the client ssh, at remote machine. 

#### test hadoop

* on master node

```
hduser@ubuntu:/usr/local/hadoop/sbin$ jps
128816 SecondaryNameNode
128563 DataNode
129156 Jps
128367 NameNode
```

* on worker node:

```
hduser@worker:/usr/local/hadoop/logs$ jps
985 Jps
831 DataNode
```


also can test with `mapreduce`






