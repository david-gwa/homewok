
[refer](https://www.jianshu.com/p/f368e8fa80ec)
[refer2](https://www.cnblogs.com/RainingNight/p/using-kubeadm-to-create-a-cluster-1-13.html)

```shell 
sudo apt-get update && sudo apt-get install -y apt-transport-https curl

sudo curl -s https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg| sudo apt-key add -

sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list

deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main

EOF

sudo apt-get update 

sudo apt-get install -y kubelet kubeadm kubectl

```

all root login and setting passwd-free remote login access for master node 


#### [aliyun k8s config](https://yq.aliyun.com/articles/702158)


* swapoff -a 
* ufw disable 
* install selinux(https://askubuntu.com/questions/481293/selinux-implementation-in-ubuntu)

```shell
apt-get remove apparmor
apt-get install selinux 
sudo sed -i 's/SELINUX=.*/SELINUX=permissive/' /etc/selinux/config
getenforce

```

* install aliyun source

```shell
apt-get update && sudo apt-get install -y apt-transport-https curlsudo curl -s https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg| sudo apt-key add -sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.listdeb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial mainEOFsudo apt-get update
sudo apt-get install -y kubelet=1.14.1-00 kubeadm=1.14.1-00 kubectl=1.14.1-00
```

root@ubuntu:~# kubeadm init --kubernetes-version=v1.15.0 --apiserver-advertise-address=192.168.0.1  --pod-network-cidr=10.244.0.0/16  




### kubeadm master node 

[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[kubelet-check] Initial timeout of 40s passed.

Unfortunately, an error has occurred:
	timed out waiting for the condition

This error is likely caused by:
	- The kubelet is not running
	- The kubelet is unhealthy due to a misconfiguration of the node in some way (required cgroups disabled)

If you are on a systemd-powered system, you can try to troubleshoot the error with the following commands:
	- 'systemctl status kubelet'
	- 'journalctl -xeu kubelet'

Additionally, a control plane component may have crashed or exited when started by the container runtime.
To troubleshoot, list all containers using your preferred container runtimes CLI, e.g. docker.
Here is one example how you may list all Kubernetes containers running in docker:
	- 'docker ps -a | grep kube | grep -v pause'
	Once you have found the failing container, you can inspect its logs with:
	- 'docker logs CONTAINERID'



Jul 10 11:00:38 ubuntu kubelet[12430]: E0710 11:00:38.241661   12430 kubelet.go:2248] node "ubuntu" not found


[the kubelet is unhealthy due to a misconfiguration of the node in some way(requied cgroups disabled)](https://stackoverflow.com/questions/54424269/how-to-fix-the-kubelet-is-unhealthy-due-to-a-misconfiguration-of-the-node-in-so)

seems kubelet service is not able to establish connection to Kubernetes api server, therefore it hasn't passed health check during installation. 


[init blocked at wait-control-plane](https://stackoverflow.com/questions/53383994/error-marking-master-timed-out-waiting-for-the-condition-kubernetes/53410468#53410468)


### kill & reset kubeadm 
```shell 
kubeadm reset -f && rm -rf /etc/kubernetes/
systemctl start kubelet && systemctl enable kubelet
```



[connection was refused](https://linuxacademy.com/community/posts/show/topic/29679-kubectl-the-connection-to-the-server-localhost8080-was-refused)




#### reinstall kubelet through  Docker.io mirror


[cdsn](https://blog.csdn.net/jinguangliu/article/details/82792617)

Warning: [WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at https://kubernetes.io/docs/setup/cri/

Error: 	[ERROR ImagePull]: failed to pull image mirrorgooglecontainers/coredns:1.3.1: output: Error response from daemon: pull access denied for mirrorgooglecontainers/coredns, repository does not exist or may require 'docker login'


/usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --cgroup-driver=cgroupfs --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.1

==> Jul 10 13:53:18 ubuntu kubelet[31614]: E0710 13:53:18.874327   31614 reflector.go:125] k8s.io/kubernetes/pkg/kubelet/kubelet.go:453: Failed to list *v1.Node: 


#### check avialable port
```shell
netstat -lnt 
```

#### configure yaml

ps -aux | grep "kube" 

 /var/lib/kubelet/config.yaml

 /etc/kubernetes/kubelet.conf --> check the server is  10.20.168...

 
####  kube apiServer 

[WARNING Hostname]: hostname "ubuntu" could not be reached

[certs] apiserver serving cert is signed for DNS names [ubuntu kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.0.1]
[certs] etcd/server serving cert is signed for DNS names [ubuntu localhost] and IPs [192.168.0.1 127.0.0.1 ::1]


Unable to connect to the server: dial tcp 192.168.0.1:6443: i/o timeout


--apiserver-advertise-address=192.168.0.1

change network-inteface to  ppss-master


[APIserver setup](https://www.kubernetes.org.cn/doc-33)



```shell
$systemctl restart kube-apiserver
$systemctl restart kube-controller-manager
$systemctl restart kube-scheduler
```

Failed to restart kube-apiserver.service: Unit kube-apiserver.service not found.




API server s run as a pod, 


### /var/lib/kubelet/config.yaml

[配置文件设置 kubelet参数](https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/)




clusterDNS: 10.96.0.10



连不上api server 




#### kubernetes 网络配置方案


### what is fuck etcd ? 

分布式一致性 键值为存储系统，用于共享配置和服务发现。

[etcd in Kube](https://jimmysong.io/kubernetes-handbook/concepts/etcd.html)

root@ubuntu:/lib/systemd/system# sudo systemctl enable etcd 
Created symlink from /etc/systemd/system/multi-user.target.wants/etcd.service to /lib/systemd/system/etcd.service.



####  systemctl  status  kubelet -l 

Active: active (running)  



kubelet 的启动参数 

--cgroup-driver=systemd --runtime-cgroups=/systemd/system.slice --kubelet-cgroups=/systemd/system.slice





配置问题:
https://blog.csdn.net/styshoo/article/details/69220086



配置etcd：
sudo mkdir -p /etc/etcd/ 

sudo vim /etc/etcd/etcd.conf 

ETCD_NAME=default ETCD_DATA_DIR="/var/lib/etcd/"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="http://192.168.56.160:2379"

root@ubuntu:/etc/kubernetes# systemctl start etcd 
Job for etcd.service failed because the control process exited with error code. See "systemctl status etcd.service" and "journalctl -xe" for details.

check "journalctl -xe" will display: `kubelet.go:2248] node "ubuntu" not found`
因为初始化kubelet时设置的master IP是错误的，才导致kubelet无法连接到master的API Server上。



root@ubuntu:/etc/kubernetes# kubeadm config view 
Get https://192.168.0.1:6443/api/v1/namespaces/kube-system/configmaps/kubeadm-config: dial tcp 192.168.0.1:6443: connect: connection refused



`kubeadm init --config kubeadm.conf`

 

root@ubuntu:/etc/kubernetes# kubeadm config print init-defaults 
apiVersion: kubeadm.k8s.io/v1beta2
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 1.2.3.4
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  name: ubuntu
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta2
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns:
  type: CoreDNS
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: k8s.gcr.io
kind: ClusterConfiguration
kubernetesVersion: v1.14.0
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
scheduler: {}


root@ubuntu:/etc/kubernetes# kubectl version 
Client Version: version.Info{Major:"1", Minor:"15", GitVersion:"v1.15.0", GitCommit:"e8462b5b5dc2584fdcd18e6bcfe9f1e4d970a529", GitTreeState:"clean", BuildDate:"2019-06-19T16:40:16Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}
The connection to the server 192.168.0.1:6443 was refused - did you specify the right host or port?


[possible solution1 ](https://stackoverflow.com/questions/45368710/kubectl-get-the-connection-to-the-server-localhost8080-was-refused-kubernetes)


root@ubuntu:~# telnet localhost 8080 
Trying 127.0.0.1...
telnet: Unable to connect to remote host: Connection refused

at the same time, can chk  /etc/kubernetes/*.conf    "10.20.132:643"....


root@ubuntu:/etc/kubernetes# kubeadm config  images list 
W0710 16:49:58.215701   23333 version.go:98] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get https://dl.k8s.io/release/stable-1.txt: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
W0710 16:49:58.215865   23333 version.go:99] falling back to the local client version: v1.15.0
k8s.gcr.io/kube-apiserver:v1.15.0
k8s.gcr.io/kube-controller-manager:v1.15.0
k8s.gcr.io/kube-scheduler:v1.15.0
k8s.gcr.io/kube-proxy:v1.15.0
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.3.10
k8s.gcr.io/coredns:1.3.1






 /etc/kubernetes/manifests/etcd-servers :  127.0.0.1:2379 
 --advertise-address = 192.168.0.1 
 /var/lib/kubelet/config.yaml   clusterDNS: 10.96.0.10


 
#### curl http/tcp test &  netstat

 `netstat` tells which port is running, and only these are listened 

 `curl` will send a http/tcp request to these ports that are running

  netstat -ln | grep 8080

 so we register `dcp server=192.168.0.1`, but it's not listened.


####
iptables -t raw -A OUTPUT -p tcp --dport 6443 -j TRACE
iptables -t raw -A PREROUTING -p tcp --dport 6443 -j TRACE
tail -f /var/log/kern.log



### last try on K8S 

when running :  `kubectl version` : 
output:  `connection to the server localhost:8080 or  192.168.0.1 was refused`

open port:  `kubectl proxy --port=8080& 

output:  
Error from server (InternalError): an error on the server ("") has prevented the request from succeeding


root@ubuntu:/etc/kubernetes/manifests# I0711 01:14:48.438686    2848 log.go:172] http: Accept error: accept tcp 127.0.0.1:8080: accept4: too many open files; retrying in 5ms
I0711 01:14:48.439265    2848 log.go:172] http: proxy error: dial tcp 127.0.0.1:8080: socket: too many open files

one possible reason: 
原因：kubenetes master没有与本机绑定，集群初始化的时候没有设置
解决办法：执行以下命令   export KUBECONFIG=/etc/kubernetes/admin.conf




### how api-server works

k8s通过kube-apiserver这个进程提供服务，该进程运行在单个k8s-master节点上。默认有两个端口。
[aliyun api-server](https://yq.aliyun.com/articles/149595)
####  本地端口

localhost:8080   
--insecure-bind-address 
--insecure-port 

#### 安全端口 non-localhost 

ud_ip:6443 

--bind-address
--secure-port 

#### 访问方式

curl  localhost:8080/api 

curl  localhost:8080/api/v1/pods

curl  localhost:8080/api/v1/services 


kubectl proxy --port=8080& 


master node  与 api-server 之间还有通信吗 ?

[k8s cluster-master](http://docs.kubernetes.org.cn/306.html#Cluster_-gt_Master)
Master组件通过非加密(未加密或认证)端口与集群apiserver通信。这个端口通常只在Master主机的localhost接口上暴露。

测试，--advertise-apiserver-address null 


#### test1

with only ppss-mater network-interface at eno1, (gwa at enp4s0f2 is disabled)
output: cannot use "0.0.0.0" as the bind address for the API Server


#### test2

with gwa enabled, run  `kubeadm init`

kubelet.conf APIserver address:  10.20.181.132:6443 

run `sudo kubectl version` as user,  

output at ubuntu: Error from server (InternalError): an error on the server ("") has prevented the request from succeeding


output at root: root@ubuntu:~# I0711 01:49:14.919589    2848 log.go:172] http: Accept error: accept tcp 127.0.0.1:8080: accept4: too many open files; retrying in 5ms
I0711 01:49:14.920189    2848 log.go:172] http: proxy error: dial tcp 127.0.0.1:8080: socket: too many open files

possible_sol: https://blog.csdn.net/dong_beijing/article/details/79527272


* ps -aux | grep "kube" , 找到 kubelet 进程号 9186
* cd /proc/$pid/fd 
* ls -lt | wc -l  #查看打开的进程数目 

(base) ubuntu@ubuntu:~$ netstat -nlt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN  

可见apiserver的localhost 端口已开，但是 https://10.20.181.132:6443 端口没有.

Master组件通过非加密(未加密或认证)端口与集群apiserver通信。这个端口通常只在Master主机的localhost接口上暴露。


#### test3 

关闭gwa, 添加 --advertise-apiserver-address=192.168.0.1 

I0711 02:35:37.288680    2848 log.go:172] http: Accept error: accept tcp 127.0.0.1:8080: accept4: too many open files; retrying in 5ms
I0711 02:35:37.289151    2848 log.go:172] http: proxy error: dial tcp 127.0.0.1:8080: socket: too many open files

root@ubuntu:~# netstat -alt 
Active Internet connections (servers and established)
tcp        0      0 127.0.1.1:domain        *:*                     LISTEN     
tcp        0      0 master:41022            worker1:2377            ESTABLISHED
tcp        0      0 localhost:http-alt      localhost:33848         ESTABLISHED
tcp6       0      0 master:7946             worker1:50846           TIME_WAIT  
非常多localhost tcp连接

 



#### what's inside kubelet-check  



