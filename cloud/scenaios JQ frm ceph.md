
## background 

currently, we add `job_queue` list inside Dockerfile by `COPY` the `job_queue` folder from local host to the docker image, which is not dynamically well, and can't support additionaly scenarios.



## ceph rbd driver for docker  

ceph can store files in three ways:

* rbd, block storage, which usually used with virtualization kvm

* object storage, through `radosgw` api, or access by boto3 APIs. 

* cephfs, mount ceph as file system


the first idea is from local host mount to remote volume(e.g. ceph storage) mount. there are a few popular [rbd-drive plugins](https://ceph.io/geen-categorie/getting-started-with-the-docker-rbd-volume-plugin/): 


* [Yp engineering](https://github.com/yp-engineering/rbd-docker-plugin)

* AcalephStorage 

* Volplugin

* [rexray.io](https://rexray.readthedocs.io/en/stable/)


check [ceph rbd driver](https://ceph.com/geen-categorie/getting-started-with-the-docker-rbd-volume-plugin/) to understand more details. 

to support rbd-driver plugin in docker, the ceph server also need support block device driver, which sometime is not avaiable, as most small ceph team would support one or another type, either objec storage or block storage. and that's our situation. so we can't go with `rbd-driver plugin`.

another way is to use [docker volume cephfs](https://gitlab.com/n0r1sk/docker-volume-cephfs), similar reason our ceph team doesn't support `cephfs`.  


## ceph object storage access 

as the ceph team can support boto3 API to access ceph, which gives us the one and only way to access scenarios: boto3.

basically the `redis_JQ` first download all scenaio files from remote ceph through boto3 APIs, then scan the downloaded files into JQ, then feed into the python executors in front.

#### s3 client 

* [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
/usr/local/bin/aws --version
```

* [s3cmd](https://github.com/s3tools/s3cmd)


#### access files in folders in s3 bucket 




```py
    def download_files(self, bucket_name, folder_name):
        files_with_prefix = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        scenario_basename = "/pythonAPI/job_queue/scenario"
        i = 0 
        for file_ in files_with_prefix["Contents"]:
            scenario_name = scenario_basename + "%d"%i + ".py"
            print(scenario_name)
            self.download_file(bucket_name, file_['Key'], scenario_name, False)
            time.sleep(0.01)
            i += 1 

```


## manage python modules

during the project, we really need take care python packages installed by `apt-get`, `pip` and `conda`, if not there will conflicts among different version of modules:

```sh
import websockets
Trackbac:
  File "/usr/lib/python3/dist-packages/websockets/compatibility.py", line 8
    asyncio_ensure_future = asyncio.async           # Python < 3.5
```

so it's better to use conda or python virtual-env to separate the different running envs. and install packages by `conda install` is better choice, than the global `apt-get install`:

* [conda install ws](https://anaconda.org/conda-forge/websockets)

* [conda install pandas](https://anaconda.org/anaconda/pandas) 

* [conda install asammdf](https://github.com/danielhrisca/asammdf)

* [conda install botocore](https://anaconda.org/conda-forge/botocore)

* [conda install sqlalchemy](https://anaconda.org/anaconda/sqlalchemy) 

* [conda install websocket-client](https://anaconda.org/anaconda/websocket-client)

* [conda install redis](https://anaconda.org/anaconda/redis)

* [conda install boto3](https://anaconda.org/anaconda/boto3)
 


#### basic of python import 


* module,  any `*.py` file, where its name is the file name 

* package,  any folder containing a file named `__init__.py` in i, its name is the name of the folder.
 

When a module named `module1` is imported, the interpreter first searches for a built-in module with that name. If not found, it then searches for a file named `module1.py` or a folder named `module1` in a list of directories given by the variable `sys.path`

`sys.path` is initialized from 3 locations:


* the directory containing the input script, or the current directory

* `PYTHONPATH` 

* the installation-dependent default


if using `export PYTHONPATH` directly, it works. but once defined in `~/.bashrc` it doesn't actually triggered in `conda` env.
it simpler to add the root directory of the project to the `PYTHONPATH` environment variable and then running all the scripts from that directory's level and changing the import statements accordingly. `import` search for your packages in specific places, listed in sys.path. and The current directory is always appended to this list



## refer

[qemu/kvm & ceph: rbd drver in qemu](https://www.cnblogs.com/sammyliu/p/5095976.html)

[基于 Ceph RBD 实现 Docker 集群的分布式存储](https://www.ibm.com/developerworks/cn/opensource/os-cn-ceph-rbd-docker-storage/index.html)

[rexray/rbd 参考](https://my.oschina.net/u/561758/blog/1813161)

[access cephFS inside docker container without mounting cephFS in host](https://stackoverflow.com/questions/22359132/access-cephfs-inside-docker-container-without-mounting-cephfs-on-the-host)


[how to use folders in s3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/using-folders.html)

[the definitive guide to python import statements](https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html)



