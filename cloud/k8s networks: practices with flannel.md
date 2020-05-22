

## backgroud

**append the following flannel test to [k8s setup 2: virtual network flannel](https://zjli2013.github.io/)**

#### preparation image for test 


need add the network tools into [previous redis image]() as the test image:

```yml

        iputils-ping \ 
        net-tools \ 
        iptables \
        iproute 

```



#### docker/pod runtime privileges


[docker runtime privilege and Linux capabilities](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)


[container capabilities in k8s](https://www.weave.works/blog/container-capabilities-kubernetes/)

In a Kubernetes pod, the names are the same, but everything has to be defined in the pod specification. When implementing this in Kubernetes, you add an array of capabilities under the securityContext tag.


```xml
      securityContext:
        capabilities:
          add:
             - NET_ADMIN
```

by default, docker doesn't allow run `iptables` inside container. and it give errors:

```sh
root@redisjq:/# iptables -t nat -L | grep INPUT 
iptables v1.6.0: can't initialize iptables table `nat': Permission denied (you must be root)
Perhaps iptables or your kernel needs to be upgraded.
```


#### iptables inside pod

```sh
root@redisjq:/redis# iptables -t filter -L 
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination  

root@redisjq:/redis# iptables  -t nat -L 
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination 
```

interesting, there is no iptables rules inside pods. then pods will use `host` iptable rules. 


#### test with redis-server 


```sh
kubectl exec -it redisjq -n lg  /bin/bash
ping localhost #ok
ping 10.255.18.3 #not 
ping 10.3.101.101 #not
ping 10.20.180.12 

ifconfig 
>>eth0,  10.4.1.46
>>lo, 127.0.0.1

```






#### flannel.d pod on both  nodes:

```sh
gwm@meng:~/k8s/lgsvl$ kubectl get pods kube-flannel-ds-amd64-85d6m  -n kube-system --output=wide
NAME                          READY   STATUS    RESTARTS   AGE   IP             NODE   NOMINATED NODE   READINESS GATES
kube-flannel-ds-amd64-85d6m   1/1     Running   5          15d   10.20.180.12   meng   <none>           <none>

gwm@meng:~/k8s/lgsvl$ kubectl get pods kube-flannel-ds-amd64-fflsl  -n kube-system --output=wide
NAME                          READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
kube-flannel-ds-amd64-fflsl   1/1     Running   154        15d   10.20.181.132   ubuntu   <none>           <none>
```

#### coredns pod in meng node 

```sh 
gwm@meng:~/k8s/lgsvl$ kubectl get pods coredns-66bff467f8-59g97  -n kube-system --output=wide
NAME                       READY   STATUS    RESTARTS   AGE   IP          NODE   NOMINATED NODE   READINESS GATES
coredns-66bff467f8-59g97   1/1     Running   4          14d   10.4.0.27   meng   <none>           <none>
```

#### redisjs pod in ubuntu's node 

```sh
gwm@meng:~/k8s/lgsvl$ kubectl get pods redisjq -n lg --output=wide 
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE     NOMINATED NODE   READINESS GATES
redisjq   1/1     Running   0          20m   10.4.1.47   ubuntu   <none>           <none>
``` 


#### pod1 ping pod2 in the same node 

**ping successfully**

#### redisjq pod1 with vip(10.4.1.47) in ubuntu ping corends pod2(10.4.0.27) with vip in meng

```sh
root@redisjq:/redis# ping 10.4.0.27 
PING 10.4.0.27 (10.4.0.27) 56(84) bytes of data.
64 bytes from 10.4.0.27: icmp_seq=1 ttl=62 time=0.757 ms
```

**ping successfully**


#### redisjq pod1(10.4.1.7) in ubuntu node ping flannel pod(10.20.181.132) in ubuntu 

```sh
root@redisjq:/redis# ping 10.20.181.132
PING 10.20.181.132 (10.20.181.132) 56(84) bytes of data.
64 bytes from 10.20.181.132: icmp_seq=1 ttl=64 time=0.127 ms
```

**ping successfuly**


#### redisjq pod1(10.4.1.7) in ubuntu node ping flannel.d pod(10.20.180.12) in meng

```sh
root@redisjq:/redis# ping 10.20.180.12 
PING 10.20.180.12 (10.20.180.12) 56(84) bytes of data. 
```

**ping failed** 



so far, pod with vip can ping any other pod with vip in the cluster, no matter in the same node or not.  pod with vip can only ping its host machine's physical IP, but pod can't ping other hostIP.

namely, the network of pod VIP inside k8s and the bridge network from pod vip to its host is set well. but the network from pod to external IP is not well.

## update iptables to allow pod access public IP 

#### cni0, docker0, eno1, flannel.1 in host machine vs eth0 in pod  

* on node1 

```sh
cni0: 10.4.1.1
docker0: 172.17.0.1
eno1: 10.20.181.132
flannel.1: 10.4.1.0
```

* on pod1, which is running on node1

```sh
eth0:  10.4.1.48
```

[pod1 -> pod2 network message flow](https://www.centos.bz/2017/06/k8s-flannel-network/)

```sh
pod1(10.4.1.48) on node1(10.20.181.132) -> cni0(10.4.1.1) -> flannel.1(10.4.1.0) -> kube-flannel on node1(10.20.181.132) -> kube-flannel on node2(10.20.180.12) -> flannel.1 on node2 -> cni0 on node2 -> pod2(10.4.1.46) on node2
```

**add the following line on both nodes**, to handle **FORWARD** internal clusterIP data to hostIP 

```sh
iptables -t nat -I POSTROUTING -s 10.4.1.0/24 -j MASQUERADE
```


after add the new rule, check inside pod:

```sh
root@redisjq:/redis# ping 10.20.180.12 
PING 10.20.180.12 (10.20.180.12) 56(84) bytes of data.
64 bytes from 10.20.180.12: icmp_seq=1 ttl=62 time=0.690 ms
root@redisjq:/redis# ping 10.20.181.132
PING 10.20.181.132 (10.20.181.132) 56(84) bytes of data.
64 bytes from 10.20.181.132: icmp_seq=1 ttl=64 time=0.108 ms
root@redisjq:/redis# ping 10.20.180.61 
PING 10.20.180.61 (10.20.180.61) 56(84) bytes of data.
64 bytes from 10.20.180.61: icmp_seq=1 ttl=126 time=0.366 ms
root@redisjq:/redis# ping www.baidu.com
ping: unknown host www.baidu.com
root@redisjq:/redis# ping 61.135.169.121   #baidu IP
PING 61.135.169.121 (61.135.169.121) 56(84) bytes of data.
64 bytes from 61.135.169.121: icmp_seq=1 ttl=51 time=8.16 ms

```


#### pod DNS setup









