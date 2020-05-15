

## kubectrl commands 

```sh
kubectl get [pods|nodes|namespaces|services|pv] --ns your_namespace

kubectl describe [pods|nodes|namespaces]

kubectl label pods your_pod  new-label=your_label

kubectl apply -f [.yaml|.json]   #creates and updates resources in the cluster

kubectl create deployment service_name --imae=service_image   #start a single instance of service

kubectl rollout history deployment/your_service  #check history of deployment 

kubectl expose rc your_sevice --port=80 --target-port=8000

kubectl autoscale deployment your_service --min=MIN_Num --max=MAX_Num

kubectl edit your_service #edit any API resource in your preferred editor 

kubectl scale --replicas=3 your_service 

kubectl delete [pod|service]

kubectl logs your_pod # dump pod logs 

kubectl run -i --tty busybox --image=busybox  -- sh  # run pod as interactive shell 

kubectl exec -ti your_pod -- ls | nslookup kubernetes.default    #run command in existing pod (1 container case) 

```

`kubectl` is pretty much like `docker` command and more. 


## manual deploy via kubectl

```sh
kubectl create ns test-busybox
kubectl run busybox --namespace=test-busybox \
                      --port=8280 \
                      --image=busybox \
                      -- sh -c "echo 'Hello' > /var/www/index.html && httpd -f -p 8280 -h /var/www/"

kubectl get pods -n test-busybox  #should display `Running`, but `Pending` 
```

* error1: pending pod

```sh
kubectl describe pods/busybox -n test-busybox
```

gives:

```sh
  Warning  FailedScheduling  <unknown>  default-scheduler  0/2 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master: }, that the pod didn't tolerate, 1 node(s) had taint {node.kubernetes.io/unreachable: }, that the pod didn't tolerate.

```

a few things to check:

* `swapoff -a` to close firewall on working node 

* `kubectl uncordon` to make node schedulable [kubectl uncordon](https://github.com/Azure/AKS/issues/856)



* error 2: failed create pod sandbox

```sh
  Warning  FailedCreatePodSandBox  25s (x4 over 2m2s)  kubelet, ubuntu    Failed to create pod sandbox: rpc error: code = Unknown desc = failed pulling image "k8s.gcr.io/pause:3.2": Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
```

solution is to copy `k8s.grc.io/pause:3.2` image to `ubuntu node`, and restart kubelet on working node.


* error 3: no network plugin CNI

```sh
networkPlugin cni failed to set up pod "busybox_test-busybox" network: open /run/flannel/subnet.env: no such file or directory
```

[a temp solution](https://github.com/kubernetes/kubernetes/issues/36575) is to cp `/run/flannel/subnet.env` from master node to worker node, then restart kubelet at the worker node. as further study, the `cp subnet.env` to worker node is not the right solution, as every time the worker node shutdown, this `subnet.env` file will delete, and won't restart when reboot the worker node the next day.

so the final solution here is to pull `quay.io/coreos/flannel` image to worker node, as well as `k8s.gcr.io/kube-proxy`. in later k8s version, `kube-proxy` is like a proxy, what's really inside is the flannel daemon. so we need both `kube-proxy` and `flannel` at worker node, to guarantee the network working.

we can see the `busybox` service is running well: 

```sh
kubectl expose pod busybox --type=NodePort   --namespace=test-busybox
kubectl get pods --output=wide -n test-busybox
NAME      READY   STATUS    RESTARTS   AGE     IP         NODE     NOMINATED NODE   READINESS GATES
busybox   1/1     Running   0          7m57s   10.4.0.3   ubuntu   <none>           <none>
kubectl get service busybox -n test-busybox
NAME      TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
busybox   NodePort   10.107.117.219   <none>        8280:32431/TCP   33s
```

but the problem here is, we can't access this service from host machine. 


#### [exposing an external IP to access an app in cluster](https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/)

to expose service externally, define the service as either`LoadBalancer` or `NodePort` type. but `LoaderBalancer` [requires external third-party: 23562](https://github.com/kubernetes/kubernetes/issues/23562) implement of load balancer, e.g. AWS. 
[why loadBalancer service doesn't work](https://stackoverflow.com/questions/44110876/kubernetes-service-external-ip-pending): if you are using a custom Kubernetes Cluster (using minikube, kubeadm or the like). In this case, there is no LoadBalancer integrated (unlike AWS or Google Cloud). With this default setup, you can only use NodePort or an Ingress Controller.


```sh
kubectl apply -f /home/gwm/k8s/busybox.yaml
kubectl get deployments hello-world  	#display info of Deployment
kubectl describe deployments hello-world
kubectl get replicasets		#display info of ReplicaSet
kubectl describe replicasets
kubectl expose deployment hello-world --type=NodePort --name=my-service  # create a service object that exposes the deployment 
kubectl get services my-service 
kubectl describe services my-service
#cleanup when test done
kubectl delete services my-service
kubectl delete deployment hello-world
```

looks the `NodePort` service doesn't work as expected: 

```sh
curl http://10.20.180.12:8280 
curl: (7) Failed to connect to 10.20.180.12 port 8280: Connection refused
```

if pods can't be cleaned by `kubectl delete pods xx`, try `kubectl delete pod <PODNAME> --grace-period=0 --force --namespace <NAMESPACE>`. 


**how to access k8s service outside the cluster**


## kubectl config 


#### [reconfigure a node's kubelet in a live cluster](https://kubernetes.io/docs/tasks/administer-cluster/reconfigure-kubelet/#automatic-rbac-rules-for-node-authorizer)

Basic workflow overview

The basic workflow for configuring a kubelet in a live cluster is as follows:

    Write a YAML or JSON configuration file containing the kubelet’s configuration.
    Wrap this file in a ConfigMap and save it to the Kubernetes control plane.
    Update the kubelet’s corresponding Node object to use this ConfigMap.


* dump configure file of each node 

```sh
  NODE_NAME="the-name-of-the-node-you-are-reconfiguring"; curl -sSL "http://localhost:8001/api/v1/nodes/${NODE_NAME}/proxy/configz" | jq '.kubeletconfig|.kind="KubeletConfiguration"|.apiVersion="kubelet.config.k8s.io/v1beta1"' > kubelet_configz_${NODE_NAME}
```

our cluster have `ubuntu` and `meng`(as leader) two nodes. with these two config files, we found two existing issues: 


1) network config on two nodes doesn' match each other

```sh
<   "clusterDomain": "xyz.abc",
---
>   "clusterDomain": "cluster.local",
<     "10.3.0.10"
---
>     "10.96.0.10"

```

after generrating the NODE config files above, we can edit these files, and then push the edited config file to the control plane:

```sh
NODE_NAME=meng; kubectl -n kube-system create configmap meng-node-config --from-file=kubelet=kubelet_configz_${NODE_NAME} --append-hash -o yaml
NODE_NAME=ubuntu; kubectl -n kube-system create configmap ubuntu-node-config --from-file=kubelet=kubelet_configz_${NODE_NAME} --append-hash -o yaml
```

after this setting up, we can check the new generated configmaps:

```sh
kubectl get configmaps -n kube-system
kubectl edit configmap meng-node-config-t442m526c5 -n kube-system
```

tips: configMaps is also an Object in k8s, just like namespace, pods, svc. but which is only in /tmp, need manually dump. 


namely:

```sh
meng-node-config-t442m526c5          1      35m
ubuntu-node-config-ghkg27446c        1      18s
```


* set node to use new configMap, by `kubectl edit node ${NODE_NAME}`, and add the following YAML under `spec`:

```yml
configSource:
    configMap:
        name: CONFIG_MAP_NAME # replace CONFIG_MAP_NAME with the name of the ConfigMap
        namespace: kube-system
        kubeletConfigKey: kubelet
```

* observe the node begin with the new configuration

```sh
kubectl get node ${NODE_NAME} -o yaml
```


2) kubectl command doesn't work at worker node

basically, worker node always report `error: Missing or incomplete configuration info.  Please point to an existing, complete config file` when running `kubectl` command. 

which needs to copy `/etc/kubernetes/admin.conf` from master to worker, then append `cat "export KUBECONFIG=/etc/kubernetes/admin.conf" >> /etc/profile` at worker node.




[organizing cluster accesss using kubecnfig files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
 

#### docker0 iptables transfer 

when starting docker engine, `docker0` VNC is created, and this vnc add its routing rules to the host's iptables. From docker 1.13.1, the routing rules of `docker0` vnc is only transfer to localhost of the host machine, namely `docker0` to any other non-localhost is forbidden, which leads to the service can only be access on the host machine, where this pod/container is running. in multi-nodes k8s, we need enable iptable FORWARD. 

append the following line to `ExecStart` line in file `/lib/systemd/system/docker.service`: 

```xml
ExecStartPost=/sbin/iptables -I FORWARD -s 0.0.0.0/0 -j ACCEPT
```

then restart docker engine: 

```sh
systemctl daemon-reload
systemctl restart docker.service

after enable docker0 iptable rules, the following test service can be accessed on both nodes. 




## virtual network flannel


#### check running flanneld 


* `/etc/cni/net.d/10-flannel.conflist` on host machine is the same as `/etc/kube-flannel/cni-conf.json` in flannel container on master node.

* `/run/flannel/subnet.env` exist in both flannel container (on master node) and in master host machine. it looks like network configure(subnet.env) is copied from container to host machine. so if there is no `flannel container` running on some nodes, these nodes won't have the right network configure. 

at master node, `HostPath` points to: /run/flannel, /etc/cni/net.d, kube-flannel-cfg (ConfigMap); while at working node(due to missing /gcr.io/flannel image), `/run/flannel/subnet.env` is missed. previously, I thought to cp this file from master node to woker node is the solution, then this file is missed every time to restart worker node. 

once copied both `kube-proxy` and `flannel` images to worker node, and restart `kubelet` at worker node, the cluster should give `Running status` of all these components. including 2 copies of `flannel`, one running on master node, and the other running on working node. 

as we are using `kubectl` to start the cluster, the actual flanneld is `/opt/bin/flanneld` from the running flannel container, and it maps NIC to the host machine. 

another thing is, `flannel` is the core of the default `kube-proxy`, so `kube-proxy` image is also required on both nodes. `coreDNS` run two copies on master node.


#### [Flannel mechanism](https://www.jianshu.com/p/165a256fb1da)


the data flow: **the sending message** go to VNC(virtual network card) `docker0` on host machine, which transfers to VNC `flannel0`. this process is P2P. the global `etcd` service maintain a iptables among nodes, which store the subnet range of each node. 2) the `flanneld` service on the special node package **the sending message** as UDP package, and delivery to target node, based on the iptables. 3) when the target node received the UDP package, it unpackage the message, and send to its `flannel0`, then transfer to its `docker0`. 


1) after flanneld started，will create `flannel.1` virtual network card. the purpose of `flannel.1` is for across-host network, including package/unpackage UDP, and maintain iptables among the nodes. 



2) each node also create `cni0` virtual network card, at the first time to run flannel CNI. the purpose of `cni0` is same as `docker0`, and it's a bridge network, used for communication in the same node. 


![image](https://www.centos.bz/wp-content/uploads/2017/06/flannel-01.png)


## deploy redis service


#### create a k8s-redis image 

```xml
# use existing docker image as a base
FROM ubuntu:16.04

# Download and install dependency
RUN apt-get update && apt-get install -y --no-install-recommends redis-server

# EXPOSE the port to the Host OS
EXPOSE 6379

# Tell the image what command it has to execute as it starts as a container
CMD ["redis-server"]
```


build the image and push to both nodes. 


#### deploy a redis-deployment

* create `redis-deployment.yaml`: 

```xml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/name: load-balancer-example
  name: kredis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: load-balancer-example
  template:
    metadata:
      labels:
        app.kubernetes.io/name: load-balancer-example
    spec:
      containers:
      - image: 10.20.181.119:5000/k8s_redis
        name: kredis
        ports:
        - containerPort: 6379
```

* expose deployment as service

```sh
kubectl create ns test-busybox
kubectl apply -f redis-deployment.yaml
kubectl get deployments redis-deployment 	#display info of Deployment
kubectl describe deployments redis-deployment
kubectl get replicasets		#display info of ReplicaSet
kubectl describe replicasets
kubectl expose deployment redis-deployment --type=NodePort --name=my-redis  # create a service object that exposes the deployment 
kubectl get services my-redis 
kubectl describe services my-redis 
kubectl get pods --output=wide
#clean up later (afer step 3)
kubectl delete services my-redis
kubectl delete deployment redis-deployment
```

#### access as pod 

```sh 
gwm@meng:~/k8s/alpine$ kubectl get pods --output=wide 
NAME                                 READY   STATUS    RESTARTS   AGE   IP          NODE     NOMINATED NODE   READINESS GATES
kredis-deployment-7567b7f4b7-wmqgd   1/1     Running   0          16h   10.4.1.18   ubuntu   <none>           <none>
gwm@meng:~/k8s/alpine$ redis-cli -p 6379
Could not connect to Redis at 127.0.0.1:6379: Connection refused
not connected> 
gwm@ubuntu:~$ redis-cli -p 6379
Could not connect to Redis at 127.0.0.1:6379: Connection refused
not connected> 
```

as we can see here, as `redis-server` as pod, won't expose any port. and pod-IP(10.4.1.18) is only accessible inside cluster

#### access as service 

```sh
kubectl get services --output=wide 
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
kredis-deploy   NodePort    10.104.43.224   <none>        6379:31962/TCP   23h   app.kubernetes.io/name=load-balancer-example
kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP          8d    <none>
root@ubuntu:~# docker container inspect 60bfd6c5ccac  | grep 31962 
root@ubuntu:~# redis-cli -p 31962 
127.0.0.1:31962> 
root@ubuntu:~# redis-cli -p 31962 -h 10.20.181.132 
10.20.181.132:31962> 
gwm@meng:~$ redis-cli -h 10.20.181.132 -p 31962 
10.20.181.132:31962>
```

so basically, we can access `redis` as service with the exposed port `31962`, and the host node's IP(10.20.181.132), (rather than the serivce cluster IP(10.104.43.224). 

tips, only check service, won't tell on which node, the pod is running. so need check the pod, and get its node's IP. 

with `docker StartExec` with `iptable FORWARD`, `redis-cli` on on both ubuntu node and meng node can access the service. 

in summary:  if we deploy service as NodePort,  we suppose to access the service with its host node's IP and the exposed port, from external/outside of k8s.


#### endpoints 

[k8s endpoints](https://theithollow.com/2019/02/04/kubernetes-endpoints/). what's the difference from endpoints to externalIP ? 


```sh
kubectl get endpoints 
NAME         ENDPOINTS           AGE
kubernetes   10.20.180.12:6443   8d
```

it gives us the kubernetes endpoints, which is avaiable on both meng and ubuntu nodes.

```sh
gwm@meng:~$ curl http://10.20.180.12:6443 
Client sent an HTTP request to an HTTPS server.
gwm@ubuntu:~$ curl http://10.20.180.12:6443 
Client sent an HTTP request to an HTTPS server.
```

not every service has `ENDPOINTS`, which gives the way to access outside of the cluster. but `NodePort` type service can bind to the running pod's host IP with the exported port.


whenever [expose k8s service](https://yq.aliyun.com/articles/679802) to either internally or externally, it goes through `kube-proxy`. when `kube-proxy` do network transfer, it has two ways: Userspace or Iptables.

clusterIP, is basically expose internnaly, with the service's cluster IP; while nodePort type, is basically bind the service's port to each node, so we can access the service from each node with the node's IP and this fixed port. 


#### apiserver 

[core of k8s: API Server](https://www.jianshu.com/p/a25e9e613f2c), is the RESTful API for resource POST/GET/DELETE/UPDATE. we can access through: 


```sh
curl apiserver_ip:apiserver_port/api
curl apiserver_ip:apiserver_port/api/v1/pods
curl apiserver_ip:apiserver_port/api/v1/services
CURL apiserver_ip:apiserver_port/api/v1/proxy/nodes/{name}/pods/
```

*  check apiServer IP

```sh 
kubectl get pods -n kube-system --output=wide
kube-apiserver-meng            1/1     Running   2          8d     10.20.180.12    meng     <none>           <none>
```

if check the `LISTEN` ports on both worker and master nodes, there are many k8s related ports, some are accessible, while some are not. 


## k8s dashboard 

[k8s dashboard](https://github.com/kubernetes/dashboard)

[dashboard doc in cn](https://kuboard.cn/install/install-k8s-dashboard.html#%E5%AE%89%E8%A3%85)

* download src

```sh
docker search kubernetes-dashboard-amd64
docker pull k8scn/kubernetes-dashboard-amd64
docker tag k8scn/kubernetes-dashboard-amd64:latest k8s.gcr.io/kubernetes-dashboard-amd64:latest 
```

* create dashboard

```sh
kubectl apply -f https://kuboard.cn/install-script/k8s-dashboard/v2.0.0-beta5.yaml 
kubectl apply -f https://kuboard.cn/install-script/k8s-dashboard/auth.yaml
```

reports error:

```sh
  Warning  Unhealthy  5m31s (x2 over 6m11s)  kubelet, ubuntu    Liveness probe failed: Get https://10.4.0.22:8443/: dial tcp 10.4.0.22:8443: connect: connection refused

```


## understand pod in k8s


#### [accessing k8s pods from outside of cluster](http://alesnosek.com/blog/2017/02/14/accessing-kubernetes-pods-from-outside-of-the-cluster/)


* hostNetwork: true

this option applies to k8s pods, which work as `--network=host` in docker env. 

options can used for create pod: `name command args env resources ports stdin tty `

[create pod/deployment using yaml](https://www.mirantis.com/blog/introduction-to-yaml-creating-a-kubernetes-deployment/)

[k8s task1: define a command and args for a container](https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/)

[templating YAML in k8s with real code](https://learnk8s.io/templating-yaml-with-code)

but `hostNetwork` is only yaml supported


* hostPort 

the container port is exposed to the external network at <hostIP>:<hostPort>. 

```xml
spec:
	containers:
		ports:
		- containerPort: 8086
		  hostPort: 8086
```

hostPort allows to expose a single container port on the hostIP. but the hostIP is dynamic when container restarted 

* nodePort 

by default, services are accessible at ClusterIP, which is an internal IP address reachable from inside the cluster. to make the service accessible from outside of the cluster, can create a `NodePort` type service. 

once this service is created, the kube-proxy, which runs on each node of the cluster, and listens on all network interfaces is instructed to accept connections on port 30000, (from any IP ?). the incoming traffc is forwardedby the kube-proxy to the selected pods in a round-robin fashion.


this service represents a static endpoint through which the selected pods can be reached. 

* Ingress

The Ingress controller is deployed as a Docker container on top of Kubernetes. Its Docker image contains a load balancer like nginx or HAProxy and a controller daemon.


#### [view pods and nodes](https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/)

* check running pods on which node 


#### resolv.conf in k8s pod 

run as interactive into a k8s pod, then check its `resolv.conf`:

```sh
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

 `10.96.0.10` is the K8S DNS server IP, which is actually the service IP of `kube-dns` service.

**interesting**, we can ping neither 10.96.0.10, nor 10.4.0.10, which is not existing service in the cluster, nor 10.3.0.10, which is the coreDNS forwarding IP.



remember during setup the k8s cluster, we had define the coreDNS forwarding to `10.3.0.10`, is this why I can't run `curl http://<ip>:<port>` works ?

check coreDNS service:

```sh
kubectl describe  pods coredns-66bff467f8-59g97 -n kube-system 
Name:                 coredns-66bff467f8-59g97
Node:                 meng/10.20.180.12
Labels:               k8s-app=kube-dns
IP:                   10.4.0.6
```

when start `coreDNS`, is actually used to relace `kube-dns`. 



## understand service in k8s 

[doc](https://kubernetes.io/docs/concepts/services-networking/service/)

Each Pod gets its own IP address, however in a Deployment, the set of Pods running in one moment in time could be different from the set of Pods running that application a moment later.

A Service in Kubernetes is a REST object, similar to a Pod. you can `POST` a Service definition to the API server to create a new instance. 

Kubernetes assigns this Service an IP address, sometimes called the `clusterIP`, 

#### Virtual IP and service proxies 

Every node in a Kubernetes cluster runs a `kube-proxy`, `kube-proxy` is responsible for implementing a form of virtual IP for Services, whose is type is any but not `ExternalName`.

#### choosing own IP for service 

You can specify your own cluster IP address as part of a Service creation request. The IP address that you choose must be a valid IPv4 or IPv6 address from within the service-cluster-ip-range CIDR range that is configured for the API server

#### discovering services 

* ENV variables 

* DNS 


#### headless services 

by explicitly specifying "None" for the cluster IP (`.spec.clusterIP`).


#### publishing services(ServiceTypes)

expose a service to an external IP address, outside of the cluster. 

service has four type:

* ClusterIP (default): expose the service on a cluster-internal IP, which is only reachable inside the cluster

* NodePort: expose the service on each node's IP at a static port(`NodePort`), to access : <NodeIP>:<NodePort>

* ExternalName: map the services to an `externalName`

* LoadBalancer: expose the service externally using third-party load balancer(googl cloud, AWS, kubeadm has none LB)


`NodePort` and `LoadBalancer` can expose service to public, or outside of the cluster.


#### external IPs

if there are external IPs that route to one or more cluster nodes, services can be exposed on those externalIPs. 







## deploy service/pod with yaml

the previous sample `busybox`, is running as `pod`, through  `kubectl run busybox` ?  so there is no external 


* [deployment obj](https://www.jianshu.com/p/6fd42abd9baa)


* [using yaml file to create service and expose to public](https://blog.csdn.net/wucong60/article/details/81699196)
some basic knowledge: 

1) pod is like container in docker, which assigned a dynamic IP in runtime, but this pod IP is only visible inside cluster 

2) service is an abstract concept of pod, which has an unique exposed IP, and the running pods belong to this service are managed hidden. 

* [pod or deployment or service](https://stackoverflow.com/questions/41325087/what-is-the-difference-between-a-pod-and-a-deployment)


both pod and deployment are full-fledged objects in k8s API. deployment manages creating Pods by means of `ReplicaSets`, namely create pods with `spec` taken from the template. since it's rather unlikely to create pods directly in a production env.

in production, you will almost never use an `object` with the type `pod`. but a `deployment` object, which needs to keep the `replicas(pod)` alive. what's use in practice are:

1) Deployment object, where to specify app containers with some specifications

2) service object


you need `service object` since pods from deployment object can be killed, scaled up and down, their IP address is not persistent. 






## refere

[kubectl cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

[deployments from k8s doc](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

[deploy tiny web server to k8s](https://jekhokie.github.io/k8s/busybox/helm/2020/04/23/small-web-server-to-k8s.html)

[k8s production best practices](https://learnk8s.io/production-best-practices)

[cni readme](https://github.com/containernetworking/cni/blob/master/SPEC.md)

[configure network plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/):

[k8s与flannel网络原理](https://www.centos.bz/2017/06/k8s-flannel-network/)

[清晰脱俗的直解K8S网络](https://network.51cto.com/art/201908/601109.htm)

 [k8s: iptables and docker0](https://shogokobayashi.com/2018/09/27/k8s-ex01-iptables-and-docker/)

 [linux docker and iptables](https://blog.csdn.net/whatday/article/details/105197120)

[controlling access to k8s APIserver](https://kubernetes.io/docs/reference/access-authn-authz/controlling-access/)

[k8s network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

















