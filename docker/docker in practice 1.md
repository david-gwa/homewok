
### background 

Docker is a great idea to package apps, the first time to try [play with docker swarm](https://zjli2013.github.io/2019/07/12/play-with-Docker-swarm-compose/), now we have more practice with Docker, as I tried to build the Docker cluster for lg-sim.



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


### Docker to support Vulkan

lg-sim 2019.09 version has used HDRP rendering, which depends on `vulkan` GPU features, which is not supported by standard `Docker-nvidia`. but which is a good way to implement cloud deployment. Once built [the Dockerfile](https://github.com/lgsvl/simulator/issues/222) to run lg-sim 2019.04, which use the standard rendering pipeline, supported by `Docker-nvidia` well.

by adding `sudo apt-get install libvulkan1` in the previous Dockerfile, will give a no-fault built. but the container runtime has errors: 

```
Vulkan error VK_ERROR_INCOMPATIBLE_DRIVER (-9) file: ./Runtime/GfxDevice/vulkan/VKContext.cpp, line: 333
Vulkan error./Runtime/GfxDevice/vulkan/VKContext.cpp:333
Vulkan detection: 0
No supported renderers found, exiting
```

there is a pre-release [docker-nvidia-vulkan](https://github.com/edowson/docker-nvidia-vulkan), which has more details control of vulkan support, and which can build all right but failed when run, due to the built image base [cudagl requires GPU brand TELSA](https://gitlab.com/nvidia/container-images/cudagl). Nvidia has provided a few images, including openGL, CUDA, [vulkan](https://gitlab.com/nvidia/container-images/vulkan)


a few lines may help:

```
/usr/lib/nvidia-384/libGLX_nvidia.s.0 

/usr/share/vulkan/icd.d

/proc/driver/nvidia/version 


```


another big try is make the server running in headless mode.


### understand docker-compose.yml


[Understand and manage Docker container volumes](https://www.ionos.com/community/server-cloud-infrastructure/docker/understanding-and-managing-docker-container-volumes/)

[what is vulkan SDK](https://www.lunarg.com/vulkan-sdk/)

[Graham blog](https://www.wihlidal.com/blog/graphics/2019-05-28-vk-rust-ray-tracing-hlsl/)




