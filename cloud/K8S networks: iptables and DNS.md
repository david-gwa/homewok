
## background

k8s networks include a few topics:

* pod to pod communication in k8s

* pod to the host node communication

* pod to external service URL

* external request to pod in k8s



previously, we  have a little understand about the data flow about the first 2 topices and the basic component of k8s(e.g. flannel, kube-proxy, coreDNS). this blog is to answer **pod to external service URL**.



## k8s pod DNS 

[DNS for services and pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) introduced four types: 


* None 

* Default， where POD derived DNS config from the host node where to run pod.

* ClusterFirst， where POD use DNS info from kube-dns or coreDNS

* ClusterFirstWithHostNet, as the name explained.


tips, **Default** is not the default DNS policy. If dnsPolicy is not explicitly specified, then **ClusterFirst** is used as default.

the purpose of pod/service DNS is used to transfer URL to IP, which is the second step after iptabels is understand successfully.


`coreDNS` is setted during `kube-adm init` with `serverDNS`. To do SNAT, the pod/service in K8S need access 

##### resolv.conf/DNS inside pod :

```sh
root@redisjq:/redis# cat /etc/resolv.conf 
nameserver 10.96.0.10
search lg.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

clearly, the pod DNS is coming from cluster, which can be check by: 

```sh
kubectl describe configmap kubeadm-config -n kube-system 

kind: ClusterConfiguration
kubernetesVersion: v1.18.2
networking:
  dnsDomain: cluster.local
  podSubnet: 10.4.0.0/16
  serviceSubnet: 10.96.0.0/12
```

and that's the reason why resolve URL failed, as clusterDNS is kind of random defined. 

the DNS failure, will give errors as following, when start pod: 

```
socket.gaierror: [Errno -3] Temporary failure in name resolution
```



## iptables in K8S 

[docker and iptables](https://docs.docker.com/network/iptables/)

you should not modify the rules Docker inserts into your iptables policies. Docker installs two custom iptables chains named `DOCKER-USER` and `DOCKER`, and it ensures that incoming packets are always checked by these two chains first

a simple test can found, `docker0` NIC is bridge is well to bind host network namespace, either export or response request externally. while with `flannel.d` NIC, pod can't access external resources.



[code review: kube-proxy iptables](https://www.bookstack.cn/read/source-code-reading-notes/kubernetes-kube_proxy_iptables.md): 

iptables has 5 tables and 5 chains.

the 5 chaines: 

```yml
    PREROUTING: before message into route, the external request DNAT.
    INPUT: message to local host or current network namespace. 
    FORWARD: message forward to other host or other network namespace.
    OUTPUT: message export from current host
    POSTROUTING: after route before NIC, message SNAT
```


the 5 tables: 


```yml
   
    filter table, used to control the network package need to ACCEPT, or DROP, or REJECT when it comes to a chain

    nat(network address translation) table, used to modify the src/target address of network package

    mangle table, used to modify IP header info of network package

    raw table, 

    security table

``` 

for k8s pods/services, mostly consider `filter` and `nat` tables. and k8s expand another 7 chains: KUBE-SERVICES、KUBE-EXTERNAL-SERVICES、KUBE-NODEPORTS、KUBE-POSTROUTING、KUBE-MARK-MASQ、KUBE-MARK-DROP、KUBE-FORWARD. 


![image](https://static.bookstack.cn/projects/source-code-reading-notes/729e704bd9fc39c9223da5185e9ef084.png)


#### network test image







## refere

[jimmy song: config K8S DNS: kube-dns](https://jimmysong.io/blog/configuring-kubernetes-kube-dns/)

[configure DNS settings in Ubuntu](https://askubuntu.com/questions/346838/how-do-i-configure-my-dns-settings-in-ubuntu-server)

[zhihu: k8s network](https://zhuanlan.zhihu.com/p/90992878)

[k8s expose service](https://www.kubernetes.org.cn/4317.html)

[k8s network advance](https://www.kubernetes.org.cn/6838.html)

[docker iptables from tencent cloud](https://cloud.tencent.com/developer/article/1140088)








