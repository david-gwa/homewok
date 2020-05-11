
## install kubeadm


* kubeadm,  used to initial cluster

* kubectl, the CLI tool for k8s 

* kubelet, run on all nodes in the cluster


all three commands are required on all nodes. check [install kube officially](https://v1-16.docs.kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)


* swapoff 

```sh
sudo swapoff -a 
```

* create a file `/etc/apt/sources.list.d/kubernetes.list` with the following content:

```xml
deb https://mirrors.aliyun.com/kubernetes/apt/  kubernetes-xenial main
```


* add gpg key 

```sh
gpg --keyserver keyserver.ubuntu.com --recv-keys BA07F4FB 
gpg --export --armor BA07F4FB | sudo apt-key add -
```

* apt install

```sh 
sudo apt-get update 
sudo apt-get install kubelet kubectl kubeadm 

```

tips, `apt-get install` will install v1.18.2. 

* restart kubelet 

```sh
systemctl daemon-reload
systemctl restart kubelet
```

if need degrade to v17.3, do the following: 

```sh
sudo apt-get install -qy --allow-downgrades kubelet=1.17.3-00
sudo apt-get install -qy --allow-downgrades kubeadm=1.17.3-00
sudo apt-get install -qy --allow-downgrades kubectl=1.17.3-00
```

#### kubeadm setup 

we setup k8s with kubeadm tool, which requires a list of images:

* check the required images to start kubeadm

```sh
kubeadm config images list
```

which returns:

```sh
k8s.gcr.io/kube-apiserver:v1.18.2
k8s.gcr.io/kube-controller-manager:v1.18.2
k8s.gcr.io/kube-scheduler:v1.18.2
k8s.gcr.io/kube-proxy:v1.18.2
k8s.gcr.io/pause:3.2
k8s.gcr.io/etcd:3.4.3-0
k8s.gcr.io/coredns:1.6.7
```

the image source above is not aviable, which can be solved by:

```sh
kubeadm config images pull --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers/
```

if the command above doesn't work well, try to `docker pull` directly and tag the name back to `k8s.gcr.io`:


```sh
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/$imageName
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/$imageName k8s.gcr.io/$imageName
```

#### start a k8s cluster 

after the preparation above, finally start a k8s cluster as:

```sh
kubeadm init --pod-network-cidr=10.4.0.0/16 --cluster_dns=10.3.0.10 
```

futher, check [kubeadm init options](https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/kubeadm-init/):

```sh
--pod-network-cidr  # pod network IP range

--service-cidr # default 10.96.0.0/12

--service-dns-domain #cluster.local

```

`cluster_dns` option is used as the cluster DNS/namespace, which will be used in the configureMap for `coreDNS` forwarding. 


if start successfully, 

* then run the following as a regular user to config safety-verficiation:

```sh
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

* check

```sh 
sudo kubectl get nodes   #both nodes are READY
sudo kubectl get pods -n kube-system  #check system
sudo kubectl describe pod coredns-xxxx  -n kube-system
```


#### add pod network

pod network, is the network through which the cluster nodes can communicate with each other.

```sh
sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

* worker node to join the new k8s cluster : 

```sh 
kubeadm reset
sudo swapoff -a 
kubeadm join 10.20.180.12:6443 --token o0pcpc.v3v8bafmbu6e4bcs \
    --discovery-token-ca-cert-hash sha256:2a15d392821f8c51416e49e6ccd5393df6f93d738b24b2132e9a9a19276f4f54 
```


then cp `flannel-cni.conflist` into worker node. `/etc/cni/net.d/10-flannel.conflist` to the same path in worker node.

if check `sudo kubectl get pods -n kube-system` :  there may come **an error: here found: coredns CrashLoopBackOff or Error**

this is due to `DNS/nameserver resolving issue in Ubuntu, where `coreDNS service` forwarding the k8s cluster service to the host `/etc/resolv.conf`, which only has `127.0.0.1`.  the cause for CoreDNS to have CrashLoopBackOff is when a CoreDNS Pod deployed in Kubernetes detects a loop. A number of [workarounds are available](https://github.com/coredns/coredns/tree/master/plugin/loop#troubleshooting-loops-in-kubernetes-clusters) to avoid Kubernetes trying to restart the CoreDNS Pod every time CoreDNS detects the loop and exits.

check the `coreDNS configMap` by :

```sh
kubectl edit cm coredns -n kube-system 
```

we see something like:

```xml
        prometheus :9153
      #  forward . /etc/resolv.conf
        forward . 10.3.0.10
        cache 30
        loop
        reload
        loadbalance
```

so modify `forward line` to `forward . 10.3.0.10`.  or to delete `loop` service there, which is not good idea.

[a very good explain](https://stackoverflow.com/questions/52645473/coredns-fails-to-run-in-kubernetes-cluster)



#### test cluster 

[test sample](https://www.bookstack.cn/read/follow-me-install-kubernetes-cluster-1.8.x/08.%E9%AA%8C%E8%AF%81%E9%9B%86%E7%BE%A4%E5%8A%9F%E8%83%BD.md)


#### clear cluster 

[clear test](https://www.bookstack.cn/read/follow-me-install-kubernetes-cluster-1.8.x/12.%E6%B8%85%E7%90%86%E9%9B%86%E7%BE%A4.md)

```sh
 sudo systemctl stop kubelet kube-proxy flanneld docker

```

## understand CNI (container network interface)

the following network plugin can be found from [k8s cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)


* backgroud

container network is used to connect (container itself) to other containers, host machine or external network. container in runtime has a few network mode:

```sh
none

host

bridge

```

CNI brings a general network framework, used to manage network configure and network resources. 




####  coreDNS

first, run coreDNS as a service in the cluster. then, update `kubelet` parameters to include IP of coreDNS and the cluster domain. 


if there is no existing running Kube-DNS, or need a different `CLusterIP` for `CoreDNS`, then need update `kubelet` configuration to set `cluster_dns` and `cluster_domain` appropriately, which can be modified at:

`/etc/systemd/system/kubelet.service/10-kubeadm.conf` with additional options appending at `kubelet` line :


```xml
--cluster_dns=10.3.0.10   --cluster_domain=cluster.local
```

* restart kubelet service 

```sh
systemctl status kubelet 
systemctl daemon-reload 
systemctl restart docker 
```

#### 




## refere

[blog: setup k8s on 3 ubuntu nodes](https://computingforgeeks.com/how-to-setup-3-node-kubernetes-cluster-on-ubuntu-18-04-with-weave-net-cni/)

[cni readme](https://github.com/containernetworking/cni/blob/master/SPEC.md)

[flannel for k8s from  silenceper](https://silenceper.com/blog/201809/flannel-in-k8s/)

[coreDNS for k8s service discovery](https://blogs.infoblox.com/community/coredns-for-kubernetes-service-discovery/)



