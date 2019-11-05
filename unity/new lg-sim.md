
## download 

error: RPC failed; curl 56 GnuTLS recv error (-54): Error in the pull function.

error: RPC failed; curl 56 GnuTLS recv error (-110): The TLS connection was non-properly terminated.

error: RPC failed; curl 18 transfer closed with outstanding read data remaining


fatal: The remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed



原因探讨：出现此问题原因 http缓存不够或者网络不稳定等。

解决方案：

1、查看当前配置命令

  git config -l

2、httpBuffer加大    

git config --global http.postBuffer 524288000

3、压缩配置

git config --global core.compression -1    

4、修改配置文件

export GIT_TRACE_PACKET=1

export GIT_TRACE=1

export GIT_CURL_VERBOSE=1


## workflow of 2019.07 version


### build instructions

[build link](https://www.lgsvlsimulator.com/docs/build-instructions/)

* build WebUI

* build simulator --> the envs and vehicles should be generated as AssetBundles

in default build, there will be download `SingleLane` map,  `Town` map and `Junga2015` vehicle, which store at /build/AssetsBundle folder


if build WebUI independently with Unity build, then the downloaded maps and vehicle is stored at /project/AssetBundles

 
### [vehicle UI](https://www.lgsvlsimulator.com/docs/vehicles-tab/#where-to-find-vehicles) 

#### how to add a vehicle ?

`Add new` button, if URL is not local, will download to local db at 

	~/.config/unity3d/LG/LGSVL/folder/to/assets


#### how to change the configuration of a vehicle ? 






### access asset.db

* install sqlite

```shell
sudo add-apt-repository ppa:jonathonf/backports

sudo apt-get update && sudo apt-get install sqlite3

```

* install sqlite broswer

```shell
sudo add-apt-repository -y ppa:linuxgndu/sqlitebrowser
sudo apt-get update
sudo apt-get install sqlitebrowser
```

## how sqlite works with webui 




### run api



in  pythonAPI subfolder, run:

```shell

./setup.py  build

./setup.py install

```

will install *.egg to  `/home/wubantu/anaconda3/envs/lg/lib/python3.7/site-packages/lgsvl-0.0.0-py3.7.egg`





