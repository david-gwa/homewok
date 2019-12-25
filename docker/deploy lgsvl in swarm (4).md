

### background 

previously, I tried to [deploy lgsvl]() in docker swarm, which is blocked by the conflict of host network to run lgsvl and the routing mesh of swarm.  


### http *

why use [--network=host](https://github.com/lgsvl/simulator/issues/488#issuecomment-553265946), is actually not a have-to, the alternative option is to use `"*"` as `Configure.webHost`, instead of `localhost` nor a special IP address, which lead o HttpListener error: 

		The requested address is not vaid in this context.


then, we can [docker run lgsvl](https://github.com/lgsvl/simulator/issues/488#issuecomment-557746438) without host network limitations.

but still, if run by `docker service create`, it still report `Error initiliazing Gtk+`. 
 

### Gtk/UI in Unity 

when starting lgsvl, it pops the resolution window, which is a plugin of Unity Editor, and implemented with `gtk`, but also lead to the failure to run lgsvl as service in docker swarm.

the simple solution is to disable resolution selection in Unity Editor.

        	Build Settings --> Player Settings -->  Disable Resolution

then the popup window is bypassed.


### ignore publish port

I tried to ignore `network host` and run directly with routing mesh, but it still doesn't work. then I remember at the previous blog, when run vkcube or glxgears in docker swarm, it actually does use `--network host`, so it looks the failure of running lgsvl in docker swarm, is not due to `network host`, but is due to `Gtk/gui`. as we can bypass the resolution UI, then directly running as following, works as expected: 
  

```
sudo docker service create --name lgsvl --generic-resource "gpu=1" --replicas 2 --env DISPLAY --mount src="X11-unix",dst="/tmp/.X11-unix" --network host lgsvl

```


### add assets into container

another update is to bind  assets from host into lgsvl image, which is stored as sqlite data.db, which is a necessary, as we bypassed the authentication, and the cluster has no access to external Internet.



### 




















