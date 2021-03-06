

##  install xserver-xorg-video-dummy 

	apt-cache search xserver-xorg-video-dummy 
	apt-get update 
	sudo apt-get install xserver-xorg-video-dummy

which depends on `xorg-video-abi-20` and `xserver-xorg-core`, so need to install `xserver-xorg-core` first. after update xorg.conf as [run Xserver using xserver-xorg-video-dummy driver](https://techoverflow.net/2019/02/23/how-to-run-x-server-using-xserver-xorg-video-dummy-driver-on-ubuntu/), and reboot the machine, which leads both keyboard and mouse doesn't reponse any more. 

### understand xorg.conf

usually, `xorg.conf` is not in system any more, so most common use, the xorg will configure the system device by default. if additional device need to configure, can run in root `X -configure`, which will generate `xorg.conf.new` file at `/root`.

there are two `xorg.conf`, one generated by running `X -configure`, which located at `/root/xorg.conf.new` ;  the other is generated by `nvidia-xconfigure`,  which can be found at `/etc/X11/xorg.conf`.


the following list is from [xorg.conf doc](https://www.x.org/releases/X11R7.7/doc/man/man5/xorg.conf.5.xhtml)

* ServerLayout section

it is at the highest level, they bind together the input and output devices that will be used in a session.

input devices are described in `InputDevice` sections, output devices usualy consist of multiple independent components(GPU, monitor), which are defined in `Screen` section.  each `Screen` section binds togethere a graphics board(GPU) and a monitor. 

the GPU are described in `Device` sections and monitors are described in `Monitor` sections


* FILES section

used to specify some path names required by the server.

e.g. ModulePath, FontPath ..

* SERVERFLAGS section

used to specify global Xorg server options.  all should be `Options`

`"AutoAddDevices"`,  enabled by default.


* MODULE section

used to specify which Xorg server (extension) modules shoul be loaded.


* INPUTDEVICE section 

Recent X servers employ HAL or udev backends for input device enumeration and input hotplugging. It is usually not necessary to provide InputDevice sections in the xorg.conf if hotplugging is in use (i.e. AutoAddDevices is enabled). If hotplugging is enabled, InputDevice sections using the mouse, kbd and vmmouse driver will be ignored.

`Identifier` and `Driver` are required in all `InputDevice` sections.  `Identifier` used to specify the unique name for this input device;  `Driver` used to specify the name of the driver.

An InputDevice section is considered active if it is referenced by an active ServerLayout section, if it is referenced by the −keyboard or −pointer command line options, or if it is selected implicitly as the core pointer or keyboard device in the absence of such explicit references. The most commonly used input drivers are evdev(4) on Linux systems, and kbd(4) and mousedrv(4) on other platforms.

a few driver-independent `Options` in `InputDevice`:

`CorePointer` and `CoreKeyboard` are the inverse of option `Floating`, which, when enabled, the input device does not report evens through any master device or control a cursor. the device is only available to clients using X input Extension API.  

* Device section

there must be at least one, for the video card(GPU) being used. `Identifier` and `Driver` are required in all `Device` sections.

* Monitor Section
there must be at least one, for the monitor being used. the default configuration will be created when one isn't specified.  `Identifier` is the only mandatory.


* Screen Section
There must be at least one, for the “screen” being used, represents the binding of a graphics device (Device section) and a monitor (Monitor section). A Screen section is considered “active” if it is referenced by an active ServerLayout section or by the −screen command line option. The `Identifier` and `Device` entries are mandatory. 


### debug keyboard/mouse not response after X upgrade


* login to Ubuntu safe mode, by `F12` -->  `Esc` (to display GRUB2 menu), then `enable network` -->  `root shell`

* run `	X -configure`

one line say:
 
	List of video drivers:  dummy, nvidia,  modesetting. 


#### uninstall xserver-xorg-video-dummy

I thought the dummy video driver is the key reason, so uninstall it, then rerun the lines above, check `/var/log/Xorg.0.log`:

```
[   386.768] List of video drivers:
[   386.768] 	nvidia
[   386.768] 	modesetting
[   386.860] (++) Using config file: "/root/xorg.conf.new"
[   386.860] (==) Using system config directory "/usr/share/X11/xorg.conf.d"
[   386.860] (==) ServerLayout "X.org Configured"
[   386.860] (**) |-->Screen "Screen0" (0)
[   386.860] (**) |   |-->Monitor "Monitor0"
[   386.861] (**) |   |-->Device "Card0"
[   386.861] (**) |   |-->GPUDevice "Card0"
[   386.861] (**) |-->Input Device "Mouse0"
[   386.861] (**) |-->Input Device "Keyboard0"
[   386.861] (==) Automatically adding devices
[   386.861] (==) Automatically enabling devices
[   386.861] (==) Automatically adding GPU devices
[   386.861] (**) ModulePath set to "/usr/lib/xorg/modules"
[   386.861] (WW) Hotplugging is on, devices using drivers 'kbd', 'mouse' or 'vmmouse' will be disabled.
[   386.861] (WW) Disabling Mouse0
[   386.861] (WW) Disabling Keyboard0
Xorg detected  mouyourse at device /dev/input/mice.
Please check your config if the mouse is still not
operational, as by default Xorg tries to autodetect
the protocol.
```

there is a warning: `(WW) Hotplugging is on, devices using drivers 'kbd', 'mouse' or 'vmmouse' will be disabled`


#### disable Hotplugging

first generate by `X -configure` at `/root/xorg.conf.new`, and copy it to `/etc/X11/xorg.conf`. then add the additional section in /etc/X11/xorg.conf, , which will disable Hotplugging: 

```
Section "ServerFlags"
Option "AllowEmptyInput" "True"
Option "AutoAddDevices" "False"
EndSection
```

however, it reports: 

```
 (EE) Failed to load module "evdev" (module does not exist, 0)
 (EE) NVIDIA(0): Failed to initialize the GLX module; please check in your X
 (EE) NVIDIA(0):     log file that the GLX module has been loaded in your X
 (EE) NVIDIA(0):     server, and that the module is the NVIDIA GLX module.  If
 (EE) NVIDIA(0):     you continue to encounter problems, Please try
 (EE) NVIDIA(0):     reinstalling the NVIDIA driver.
 (EE) Failed to load module "mouse" (module does not exist, 0)
 (EE) No input driver matching `mouse'
```

#### switch to nvidia xorg.conf

which reports:

```
(EE) Failed to load module "mouse" (module does not exist, 0)
(EE) No input driver matching `mouse'
(EE) Failed to load module "evdev" (module does not exist, 0)
(EE) No input driver matching `evdev'
```

it fix the Nvidia issue, but still can't fix the input device and driver issue.


#### switch to evdev driver

as mentioned previously, `evdev` driver is the default driver for Linux, and will be loaded by Xserver by default. so try to both Keyboard and Mouse driver to `evdev`,

which reports:


```
 (EE) No input driver matching `kbd'
 (EE) Failed to load module "kbd" (module does not exist, 0)
 (EE) No input driver matching `mouse'
 (EE) Failed to load module "mouse" (module does not exist, 0)
```

looks it's the problem of driver, even the default driver is missed. I try to copy master node's [/usr/lib/xorg/modules/input/](https://forums.gentoo.org/viewtopic-p-4771817.html) to worker node, then it reports :


```
(EE) module ABI major version (24) doesn't match the server's version (22)
(EE) Failed to load module "evdev" (module requirement mismatch, 0)
```


which can be fixed by adding `Option IgnoreABI` .


#### delete customized keyboard and mouse 

if enable Hotplugging, the X will auto detect the device, I'd try: 

```
Section "ServerLayout"
    Identifier     "Layout0"
    Screen      0  "Screen0" 0 0 
EndSection


Section "Monitor"
    Identifier     "Monitor0"
    VendorName     "Unknown"
    ModelName      "Unknown"
    HorizSync       28.0 - 33.0
    VertRefresh     43.0 - 72.0
    Option         "DPMS"
EndSection

Section "Device"
    Identifier     "Device0"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
EndSection

Section "Screen"
    Identifier     "Screen0"
    Device         "Device0"
    Monitor        "Monitor0"
    DefaultDepth    24
    SubSection     "Display"
        Depth       24
    EndSubSection
EndSection

Section "ServerFlags"
  Option "AllowEmptyInput" "True"
  Option "IgnoreABI" "True"
EndSection

```

which reports:

```
 (II) No input driver specified, ignoring this device.
 (II) This device may have been added with another device file.
 (II) config/udev: Adding input device Lenovo Precision USB Mouse (/dev/input/mouse0

```

there is no ERROR any more, but looks the default Input driver (evdev?) can't be found out ...


#### reinstall xorg

Mouse and keyboard can be driven by evdev or mouse/keyboard driver respectively. Xorg will load only `endev` automatically, To use mouse and/or keyboard driver instead of evdev they must be loaded in xorg.conf. There is no need to generate xorg.conf unless you want to fine tune your setup or need to customize keyboard layout or mouse/touchpad functionality.

* firstly configure new network interface for worker node:

[configure DHCP network connection](https://unix.stackexchange.com/questions/303536/configuring-automatic-dhcp-network-connection-via-command-line-on-ubuntu-14-04)

setting at `/etc/network/interface`:

```
auto enp0s25 
iface enp0s25 inet dhcp
```

ifconfig enp0s25 down
ifconfig enp0s25 up
 
* then reinstall xorg: 

```
sudo apt-get update 
sudo apt-get upgrade
sudo apt-get install xserver-xorg-core  xserver-xorg  xorg
``` 

which install these libs, `xserver-xorg-input-all`, `xserver-xorg-input-evdev`,  `xserver-xorg-inut-wacom`, `xserver-xorg-input-vmouse`,  `xserver-xorg-input-synaptics`, these are the exact missing parts(input device and drivers).  it looks when uninstall `video-dummy`, these modules are deleted by accident.


* reboot, both keyboard and mouse work !

* "sudo startx" through ssh

now the user password doesn't work in normal login, but when ssh login from another machine, the password verify well. which can be fixed by ssh login from remote host first, then run `sudo startx`, which will bring the user-password verification back


## virtual display 


[xdummy](https://xpra.org/trac/wiki/Xdummy)

[xdummy: xorg.conf](http://xpra.org/xorg.conf)

run: `Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./10.log -config ./xorg.conf :10` 

* test with glxgears/OpengGL works

1) DISPLAY=localhost:10.0  works

2) DISPLAY=:0  works, but you can't see it, cause the worker host is in virtual display

* test with vkcube/Vulkan failed


in summary, the vitual display can support OpenGL running, but doesn't support Vulkan yet. [unity simulation cloud SDK](https://unity.com/simulation) is the vendor's solution, but licensed.



## refer

[sample xorg.conf for dummy device](http://xpra.org/xorg.conf)

[Keyboard and mouse not responding at reboot after xorg.conf update](https://askubuntu.com/questions/940476/keyboard-and-mouse-not-responding-at-reboot-after-xorg-conf-update)

[how to Xconfigure](https://askubuntu.com/questions/4662/where-is-the-x-org-config-file-how-do-i-configure-x-there)

[no input drivers loading in X](https://www.linuxquestions.org/questions/linux-software-2/no-input-drivers-loading-in-x-4175577628/)
