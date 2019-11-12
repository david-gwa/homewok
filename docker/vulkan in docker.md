
### background 

Docker is a great idea to package apps, the first time to try [play with docker swarm](https://zjli2013.github.io/2019/07/12/play-with-Docker-swarm-compose/). [lg-sim](https://github.com/lgsvl/simulator) has updated to HDRP rendering, which has a higher quality, as well requires more GPU features, `Vulkan`. currently `Vulkan` is not supported by standard `docker` neither `nvidia-dcker`, which is deprecated after `docker enginer > 19.03`. 

the previous lg-sim(2019.040 can be easily run in docker, as mentioned [here](https://github.com/lgsvl/simulator/issues/222).

there is [nvidia images](https://gitlab.com/nvidia/container-images),  the special one we are interesed is [vulkan docker](https://gitlab.com/nvidia/container-images/vulkan), and there is an related [personal project](https://github.com/edowson/docker-nvidia-vulkan), which is based on the `cudagl=10.1`, which is not supported by non-Tesla GPU. so for our platform, which has only [Qudra P2000 GPUs](https://developer.nvidia.com/cuda-gpus), the supported CUDA is 9.0, so we need to rebuild the vulkan docker based on `CUDA9.0`. check the [vulkan dockerfile](https://gitlab.com/nvidia/container-images/vulkan/blob/master/Dockerfile), instead of using `cudagl:9.0`, change to: `FROM nvidia/cudagl:9.0-base-ubuntu16.04`

after build the image, we can build the [vulkan test samples](https://gitlab.com/nvidia/container-images/samples/tree/master/vulkan/ubuntu16.04). if no issue, load lg-sim into this vulkan-docker.


a few lines may help:

```
/usr/lib/nvidia-384/libGLX_nvidia.s.0 

/usr/share/vulkan/icd.d

/proc/driver/nvidia/version 


```


### VOLUME in dockerfile

the following sample is from [understand VOLUME instruction in Dockerfile](https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile)

create a Dockerfile as: 

```
	FROM openjdk
	VOLUME vol1 /vol2
	CMD ["/bin/bash"]
```


```
docker build -t vol_test . 
docker run --rm -it vol_test 
```


check in the container, `vol1`, `vol2` does both exist in the running container.

```
bash-4.2# ls 
	bin   dev  home  lib64	mnt  proc  run	 srv  tmp  var	 vol2
	boot  etc  lib	 media	opt  root  sbin  sys  usr  vol1
```



also check in host terminal:

``` 
root@ubuntu:~# docker volume ls 
DRIVER              VOLUME NAME
local               0ffca0474fe0d2bf8911fba9cd6b5875e51abe172f6a4b3eb5fd8b784e59ee76
local               7c03d43aaa018a8fb031ef8ed809d30f025478ef6a64aa87b87b224b83901445

```

and check further: 

```
root@ubuntu:/var/lib/docker/volumes# ls 
0ffca0474fe0d2bf8911fba9cd6b5875e51abe172f6a4b3eb5fd8b784e59ee76  metadata.db
7c03d43aaa018a8fb031ef8ed809d30f025478ef6a64aa87b87b224b83901445
```

once `touch ass_file` under container `/vol1`, we can find immediately in host machine at `/var/lib/docker/volumes` :
 
```
root@ubuntu:/var/lib/docker/volumes/0ffca0474fe0d2bf8911fba9cd6b5875e51abe172f6a4b3eb5fd8b784e59ee76/_data# ls -lt 
total 0
-rw-r--r-- 1 root root 0 Nov  7 11:40 css_file
-rw-r--r-- 1 root root 0 Nov  7 11:40 ass_file

```

also if deleted file from host machine, it equally delete from the runnning container. The `_data` folder is also referred to as a `mount point`.  Exit out from the container and list the volumes on the host. They are gone. We used the --rm flag when running the container and this option effectively wipes out not just the container on exit, but also the volumes.


### sync localhost folder to container 

by default, Dockerfile can not map to a host path, when trying to bring files in from the host to the container during runtime. namely, The Dockerfile can only specify the destination of the volume.  for example, we expect to sync a localshost folder e.g. `attach_me` to container, by `cd /path/to/dockfile && docker run -v /attache_me -it vol_test`. a new data volume named `attach_me` is, just like the other `/vol1`, `/vol2` located in the container, but this one is totally nothing to do with the localhost folder. 


while a trick can do the sync:

```
docker run -it -v $(pwd)/attach_me:/attach_me vol_test
```

Both sides of the `:` character expects an absolute path. Left side being an absolute path on the host machine, right side being an absolute path inside the container.


### volumes in compose

which is only works during compose build, and has nothing to do with docker container.


### copy folder from host to container 

* COPY in dockerfile

ERROR: Service 'lg-run' failed to build: COPY failed: stat /var/lib/docker/tmp/docker-builder322528355/home/wubantu/zj/simulator201909/build: no such file or directory

the solution is to keep the folder in Dockerfile's current pwd; if else, Docker engine will look from `/var/lib/docker/tmp`.


### VOLUME summary

If you do not provide a volume in your run command, or compose file, the only option for docker is to create an anonymous volume. This is a local named `volume with a long unique id` for the name and no other indication for why it was created or what data it contains. If you override the volume, pointing to a named or host volume, your data will go there instead.

when `VOLUME` in DOCKERFILE, it actually has nothing to do with current host path, it actually generate something in host machine, located at `/var/lib/docker/volumes/`, which is nonreadable and managed by Docker Engine. also don't forget to use `--rm`, which will delete the attached volumes in host when the container exit.


[warning: VOLUME breaks things](https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile)







### understand docker-compose.yml


[Understand and manage Docker container volumes](https://www.ionos.com/community/server-cloud-infrastructure/docker/understanding-and-managing-docker-container-volumes/)

[what is vulkan SDK](https://www.lunarg.com/vulkan-sdk/)

[Graham blog](https://www.wihlidal.com/blog/graphics/2019-05-28-vk-rust-ray-tracing-hlsl/)




