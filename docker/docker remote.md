
the gtk lib error happens at Ubuntu host: 

root@c518840d1a00:~/.config/unity3d/LG Silicon Valley Lab/Automotive Simulator# cat Player.log 
Error loading /lg/simulator_Data/Plugins/x86_64/ScreenSelector.so: libgtk-x11-2.0.so.0: cannot open shared object file: No such file or directory
Desktop is 0 x 0 @ 0 Hz


key/value storage for  cluster 


swarm-distribution-log https://yq.aliyun.com/articles/517847



[ubuntu@ubuntu ~]$ docker-machine create --driver generic --generic-ip-address=192.168.0.1 ppss-master 
Creating CA: /home/wubantu/.docker/machine/certs/ca.pem
Creating client certificate: /home/wubantu/.docker/machine/certs/cert.pem
Running pre-create checks...
Creating machine...
(ppss-master) No SSH key specified. Assuming an existing key at the default location.
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Error creating machine: Error detecting OS: Too many retries waiting for SSH to be available.  Last error: Maximum number of retries (60) exceeded








### update GPU driver for tsuipc 


341 -->  361 


 /var/log/nvidia-installer.log  -->  binary package for nvidia(361.93.03) not found 

/var/lib/dkms/nvidia/361.93.03/build/make.log 


### stop X server during Nvidia update
https://unix.stackexchange.com/questions/25668/how-to-close-x-server-to-avoid-errors-while-updating-nvidia-driver

 sudo service lightdm stop 
 sudo  systemctl restart lightdm.service   (doesn't get the screen back)



 dkms status | grep -i "nvidia" 

==>   nvidia-340 ,  installed 
      nvidia, 361, added

 

Ubuntu 16 stuck in login loop after installing nvidia36 driver
https://askubuntu.com/questions/762831/ubuntu-16-stuck-in-login-loop-after-installing-nvidia-364-drivers


sudo ifconfig usb0 up  to enable networking...


/etc/init.d/networking restart  

[failed]

restarting networking:  networking.serviceJob for networkin.service failed because the control process exited with error code.   

Systemctl status networking.service  or  journalctl -xe 



service lightdm restart doesn't work





### display manager 

the default one:   /etc/X11/default-display-manager :: /usr/sbin/lightdm

$ sudo telinit 5
$ sudo service lightdm restart
$ sudo systemctl start lightdm

to start GUI:

sudo systemctl  start lightdm.service 

Gnome not start up, afteer install  nvidia-364.391...

$ startx 

systemd-logind: Failed to fully start up daemon: Input/Output error

vesa: Igoring device with a bound kernel driver 
Fatal server eror:  (EE) no screens found 
please check log file at "/var/log/Xorg.0.log" for additional information
Server terminated with error(1), Closing log file
xinit: giving up
xinit: unable to connect to X server: Connection refused
xinit: server error 



====> 


LoadModule: "glx"
NVIDIA GLX module 261.93.03 
LoadModule: "nvidia"
LoadModule: "nouveau"
LoadModle: "vesa" 

====> 

 NVIDIA: Failed to initialize the NVIDIA kernel module, please see the system's kernel log for additional eror messages 
 
 [drm] Failed to open DRM device for (null) : -22 
 
 

===>  sudo lshw -C display

hwinfo --gfxcard --short 



### even can't remove nvidia drivers


sudo apt-get purge nvidia-*

"""

E: unable to locate pacakge nvidia-installer.log
E: Couldn' find any package by glob  'nvidia-insaller.log'
E: Unable to locate package nvidia-prime-upstart.log 


"""

NVIDIA-Linux-x86-310.19.run --uninstall




### attach volume to yml or Dockerfile ? 

[stackoverflow](https://stackoverflow.com/questions/40567451/dockerfile-vs-docker-compose-volume)

`VOLUME` in Dockerfile creates a mount point but initially only maps it to Docker's internal data directory 

`volumes` in docker-compose.yml, maps te volumes to the host filesystem



### *.whl is not a valid name 


[failure due to alsa-util](https://bbs.archlinux.org/viewtopic.php?id=94696)

	sudo apt-get install alsa-utils

still: ALSA lib confmisc.c:768:(parse_card) cannot find card '0'

[same issue report](https://github.com/cypress-io/cypress-docker-images/issues/52)

due to [virtual machine](https://github.com/cypress-io/cypress-docker-images/issues/52), has no physical sound driver.. 


https://www.alsa-project.org/main/index.php/Matrix:Module-dummy





[failure due to gtk](https://askubuntu.com/questions/342202/failed-to-load-module-canberra-gtk-module-but-already-installed)

sudo apt install libcanberra-gtk-module libcanberra-gtk3-module



### remote deployment 

```shell 
chown lg-run.zip  ubuntu:wubantu 

scp lg-run.zip tsui@tsuipc:~/zj 

docker load -i  lg-run.zip 

```


on Tsuipc, in docker container:

```shell

glxgears 

Error: couldn't find RGB GLX visual or fbconfig 

sudo apt-get remove --purge xserver-xorg

sudo apt-get install xserver-xorg

sudo dpkg-reconfigure xserver-xorg

sudo reboot

```

 ldd /usr/bin/glxinfo 




[sudo nvidia-xconfig](https://askubuntu.com/questions/864730/couldnt-find-rgb-glx-visual-or-fbconfig)



ssh: connect to host tsuipc port 22: Connection refused
 


Error: couldn't get an RGB, Double-buffered visual  


[ GLX is the extension of the X11 protocol for making OpenGL work in X11 windows. There are 3 parts to a GLX enabled system:](https://stackoverflow.com/questions/8545291/opengl-glx-extension-not-supported)

apt-get install xserver-xorg-video-intel libgl1-mesa-dri libgl1-mesa-glx

[refer1](https://forums.linuxmint.com/viewtopic.php?t=212115)



/etc/X11/xorg.conf ?




/usr/lib/ | grep -ir "libgl"  * 




### on tsuipc




cp   libGLX_nvidia.so.384.130 from host to container 

cp libnvidia-tls.so.384.130

cp libnvidia-glcore.so.384.130 

sudo docker cp  /usr/lib/nvidia-384/libGLX_nvidia.so.384.130  $containerID:/usr/lib/x8_64-linux-gnu/

ln -s   libGLX_nvidia.so.38.130 libGLX_nvidia.so.0 

ln -s libGLX_nvidia.so.38.130 libGLX_indirect.so.0 



still errors:

recvfrom(3, 0x10348b0, 8, 0, NULL, NULL) = -1 EAGAIN (Resource temporarily unavailable)
poll([{fd=3, events=POLLIN}], 1, -1)    = 1 ([{fd=3, revents=POLLIN}])


open("/etc/nvidia/nvidia-application-profiles-rc.d/", O_RDONLY) = -1 ENOENT (No such file or directory)




running lg-sim in Docker at tsuipc, with the same error as [Nvidia OpenGL lib](https://gitee.com/GWM_ADS_SIM/cloud-based-ADS-simulation/issues/IYJ3H)




Desktop is 1280 x 1024 @ 60 Hz
Unable to find a supported OpenGL core profile
Failed to create valid graphics context: please ensure you meet the minimum requirements
E.g. OpenGL core profile 3.2 or later for OpenGL Core renderer
No supported renderers found, exiting

(Filename: Line: 590)


lspci | grep VGA  (no need)
error while loading shared libaries: libpci.so.3 






