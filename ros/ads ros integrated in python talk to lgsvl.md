

## background 

previously, we had done ADS ros package directly talk with lgsvl. the step further is to trigger ADS ros from scenario python script

a few requirements:

  * for ADS ros should be integrated with each scenario python script, which means, when the python script finished, the ADS ros should exit

  * the ads ros package shell script is independ of python script 

  
#### execute shell in Python 


* to [call a shell command](http://dreamsyssoft.com/python-scripting-tutorial/shell-tutorial.php) directly with `os.system(cmd)` or 

```
subprocess.call("ls -lt", shell=True)
```


* to run shell script with a python subprocess 

```
proc=subprocess.Popen([""], stdout=subprocess.PIPE)

```


`subprocess.Popen()` return the process object


a few helpful commands to debug rosrun:

```
ps -aux | grep "roscore"  

ps -aux | grep "rosmaster"

killall -9 roscore 

killall -9 rosmaster

```


## ros1 to python3

there is an real issue, due to the ADS ros package is mostly implemented by ROS1, maintained by the algorithm team. but lgsvl scenario is running with python3. [ROS1 matches Python2](http://design.ros2.org/articles/changes.html). so there comes the solution, either to upgrade the ADS ros pakcage to ROS2, or find a way to run ROS1 in python3 env.

 
#### conda base env 

we had decided to adapt ROS1 in python3 env. as the host machine has conda env, first need to [disable conda base](https://stackoverflow.com/questions/54429210/how-do-i-prevent-conda-from-activating-the-base-environment-by-default). 

```
conda config --set auto_activate_base false

```

as lgsvl scenario is runned with conda python3 env, inside which used `subprocess` to run ADS ros shell, in which creates a few new `gnome-terminal`s, which are non log-in terminal, and the trick things here: even though disabled auto activate base, and the terminal has no header `(base)`, but when check the python path, it still points to the `conda/bin/python`, which will fail `rosbridge_launch.server`, which is a pure ros1 and python2 module.

so need check if `conda --version` in the ads ros shell script is  in current terminal, if does, run `conda deactivate`, which gives error:


```
CommandNotFoundError: Your shell has not been properly configured to use 'conda deactivate'.
```

it looks there is some mess up, with init `conda.sh` is in `~/.bashrc`, but during the new terminal ceated, it doens't confgiure all right. which can be fixed :


```
conda --version 
if [ $? == 0 ]
then 
    source ~/anaconda3/etc/profile.d/conda.sh
    conda deactivate
fi 

```

in this way, we run lgsvl scenario in python3, as well as can new with python2 terminals to run ads ros nodes from this python3 terminal
  

#### ros scripts path is not python path

as we try to separate python scripts from ads ros nodes, so need some global env variable for the ros scripts path. 


## kill all ros nodes gracefully


we need restart/shutdown the ads ros nodes package at each time when python scenario script start/stop, which has two steps:

* to shutdown ros nodes, e.g.  [rosnode kill](https://answers.ros.org/question/237862/rosnode-kill/)

* to close all the gnome-terminals to run the ros nodes


the second step is very tricky, need some understand. A terminal is a file. Like /dev/tty. Files do not have a process id. The process that "owns" the terminal is usually called the controlling process, or more correctly, the process group leader. `gnome-terminal` [runs a single pid](https://askubuntu.com/questions/775025/how-to-detect-the-number-of-opened-terminals-by-the-user), it creates a child process for each and every window and/or tab. and can retrieve these child processes by the command:

		$ pgrep -P <pid_of_gnome-terminal>

Many terminals seem to [mask themselves as xterm-compatible](https://askubuntu.com/questions/640096/how-do-i-check-which-terminal-i-am-using), which is reported by echo $TERM or echo $COLORTERM. 



```
    $! is the PID of the last backgrounded process.
    kill -0 $PID checks whether it's still running.
    $$ is the PID of the current shell.
```

```
#! /bin/bash

gnome_pid=`pgrep gnome-terminal`
subpids=`pgrep -P ${gnome_pid}`

if [ ! $1 ]; then
   echo "missing the gnome-terminal pid, exit"
   exit -1
fi

#shutdown the ros nodes 
rosnode kill -a  > /dev/null  2>&1
killall -9 rosmaster > /dev/null  2>&1

#shutdown the terminals where ros nodes hosted
for pid in $subpids
do
        if [[ $pid != $1 ]] ; then
                echo $pid
                kill $pid
        fi
done


``` 

tips: the implement has a litle problem when integrate with lgsvl when the simulation time is short, e.g. 1sec, then `ros_clear.sh` can't catch the opened gnome-terminals from `ros_start.sh`. 


#### [find the process name using PID](https://www.tecmint.com/find-process-name-pid-number-linux/)

		$ ps aux | grep PID
		$ ps -p PID -o format 		
		$ curpid=`ps -p $$ -o ppid=`


#### [the output of ps aux](https://www.computernetworkingnotes.com/linux-tutorials/ps-aux-command-and-ps-command-explained.html)


+ -->  in the foreground process group
s -->  is a session leader 



## refer

[pythn subprocess from Jianshu](https://www.jianshu.com/p/2eb33b491024)

[understand linux process group](https://www.cnblogs.com/vamei/archive/2012/10/07/2713023.html)

[pidof command](https://www.cyberciti.biz/faq/linux-pidof-command-examples-find-pid-of-program/)

[which_term](https://askubuntu.com/questions/476641/how-can-i-get-the-name-of-the-current-terminal-from-command-line/476663#476663)

[get the info of a PID](https://stackoverflow.com/questions/9378021/how-to-get-process-details-from-its-pid)

[get the pid of running terminal](https://askubuntu.com/questions/476641/how-can-i-get-the-name-of-the-current-terminal-from-command-line)



