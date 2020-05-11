
## default dns/server/api namespace 

* [pod DNS vs service DNS](https://kubernetes.io/zh/docs/concepts/services-networking/dns-pod-service)


* [customizing DNS service: coredns](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/#coredns)


check the [github issue1292: coredns CrashLoopBackOff due to dnsmasq](https://github.com/kubernetes/kubeadm/issues/1292)

a few things may confused:

* dnsmasq vs NetworkManager

* /etc/resolv.conf vs  /etc/NetworkManager/*.conf 


[coredns pods have CrashLoopBackOff or Error state](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#coredns-pods-have-crashloopbackoff-or-error-state)


* use a new docker

* disable SELinux 

* modify `coredns` deployment to set `allowPrivilegeEscalation: true`



#### coreDNS

[coreDNS git](https://coredns.io)

[coreDNS](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) is DNS server that can serve as the Kubernetes cluster DNS

* where is CoreDNS configuration (“Corefile”) ? 

* deploy k8s with kubeadm with CoreDNS 


```sh
/usr/libexec/
/etc/kubernetes/
```



* [cni readme](https://github.com/containernetworking/cni/blob/master/SPEC.md)

* [configure network plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/):


### Flannel 

[multi-host networking overlay with Flannel](https://docker-k8s-lab.readthedocs.io/en/latest/docker/docker-flannel.html)

the simplest backend is UDP and uses a TUN device to encapsulate every IP fragement in a UDP packet, forming an overlay network.

[flannel github proj](https://github.com/coreos/flannel)


[flannel for k8s from  silenceper](https://silenceper.com/blog/201809/flannel-in-k8s/)


[k8s etcd arch and implementation](http://jolestar.com/etcd-architecture/)


the common error here is `worker node in NotReady status`, which is due to the worker node missed CNI plugin configure.






## k8s arch 

learning from [k8s arch](https://www.bookstack.cn/read/follow-me-install-kubernetes-cluster-1.8.x/00.Kubernetes%E4%BB%8B%E7%BB%8D.md)


![image](https://static.bookstack.cn/projects/follow-me-install-kubernetes-cluster-1.8.x/images/components.png)


## deploy pod in k8s 

#### [properties can set for a container]()




## deploy service in k8s 

* how to create a service pod ? 


#### kubectrl commands 

```sh

kubectl get [pods|nodes|namespaces|services|pv]

kubectl get pods --namespace your_namespace

kubectl describe [pods|nodes|namespaces]

kubectl label pods your_pod  new-label=your_label

kubectl apply -f [.yaml|.json]   #creates and updates resources in the cluster

kubectl create deployment service_name --imae=service_image   #start a single instance of service

kubectl rollout history deployment/your_service  #check history of deployment 

kubectl rollout undo deployment/your_service --to-revision=x #rollback to the previous deployment 

kubectl expose rc your_sevice --port=80 --target-port=8000

kubectl autoscale deployment your_service --min=MIN_Num --max=MAX_Num

kubectl edit your_service #edit any API resource in your preferred editor 

kubectl scale --replicas=3 your_service 

kubectl delete [pod|service]

kubectl logs your_pod # dump pod logs 

kubectl run -i --tty busybox --image=busybox  -- sh  # run pod as interactive shell 

kubectl attach busybox -c busybox -i -t # resume into interactive shell when the pod is running

kubectl run nginx --image=nginx --restart=Never -n yournamespace #run pod nginx in a specific namespace 

kubectl exec -ti your_pod -- ls | nslookup kubernetes.default    #run command in existing pod (1 container case) 

kubectl exec your_pod -c your_container -- ls /  # run command in existing pod (multi-container case)

kubectl cluster-info # display address of the master and services 

kubectl cluster-info dump --output-directory=/path/to/cluster/state # dump current cluster state to stdout 

kubectl api-resources --namespaced=true -o name 

```


#### manual deploy via kubectl

```sh
kubectl create ns test-busybox
kubectl run busybox --namespace=test-busybox \
                      --port=8280 \
                      --image=busybox \
                      -- sh -c "echo 'Hello' > /var/www/index.html && httpd -f -p 8280 -h /var/www/"

kubectl get pods -n test-busybox  #should display `Running`, but `Pending` 
```

* pending pod ?

```sh
kubectl describe pods/busybox -n test-busybox
```

gives:

```sh
  Warning  FailedScheduling  <unknown>  default-scheduler  0/2 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master: }, that the pod didn't tolerate, 1 node(s) had taint {node.kubernetes.io/unreachable: }, that the pod didn't tolerate.

```


which is [due to the master node is not allowd to run pod](https://linjinbao66.github.io/2020/2020-05-03-k8s%E7%AC%94%E8%AE%B0/)


further, found `ubuntu node status NotReady`. --> which is due to missing `swapoff -a`


[how to handle unschedulable nodes](https://github.com/Azure/AKS/issues/856): `kubectl uncordon`


* error 2

```sh
  Warning  FailedCreatePodSandBox  25s (x4 over 2m2s)  kubelet, ubuntu    Failed to create pod sandbox: rpc error: code = Unknown desc = failed pulling image "k8s.gcr.io/pause:3.2": Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
```


which need to copy all `k8s.grc.io` images to `ubuntu node` as well. 

* error 3

```sh
networkPlugin cni failed to set up pod "busybox_test-busybox" network: open /run/flannel/subnet.env: no such file or directory
```


[sol](https://github.com/kubernetes/kubernetes/issues/36575), cp `/run/flannel/subnet.env` from master node to worker node, then restart the pod 


finally, check the describe again:

```sh
Events:
  Type    Reason     Age        From               Message
  ----    ------     ----       ----               -------
  Normal  Scheduled  <unknown>  default-scheduler  Successfully assigned test-busybox/busybox to ubuntu
  Normal  Pulling    3m19s      kubelet, ubuntu    Pulling image "busybox"
  Normal  Pulled     31s        kubelet, ubuntu    Successfully pulled image "busybox"
  Normal  Created    30s        kubelet, ubuntu    Created container busybox
  Normal  Started    30s        kubelet, ubuntu    Started container busybox

```

* test continue 

```sh
gwm@meng:~$ kubectl expose pod busybox --type=NodePort \
>                              --namespace=test-busybox
service/busybox exposed
gwm@meng:~$ kubectl get pods --output=wide -n test-busybox
NAME      READY   STATUS    RESTARTS   AGE     IP         NODE     NOMINATED NODE   READINESS GATES
busybox   1/1     Running   0          7m57s   10.4.0.3   ubuntu   <none>           <none>
gwm@meng:~$ kubectl get service busybox -n test-busybox
NAME      TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
busybox   NodePort   10.107.117.219   <none>        8280:32431/TCP   33s
```

* check LISTEN port: `netstat -tulpn | grep LISTEN`

* the basic idea here is to find out the physical machine, on which busybox pod is running, and use the physical machine's IP to access the pod. Question, is hostmachine's IP can is passing through the pod IP, who is running on this host machine ? 

* another possible solution, is add cluster/pod DNS to the nameserver at host machine? but is this the common way ? 


##### [exposing an external IP to access an app in cluster](https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/)

```sh
kubectl apply -f /home/gwm/k8s/busybox.yaml
kubectl get deployments hello-world  	#display info of Deployment
kubectl describe deployments hello-world
kubectl get replicasets		#display info of ReplicaSet
kubectl describe replicasets
kubectl expose deployment hello-world --type=LoadBalancer --name=my-service  # create a service object that exposes the deployment 
kubectl get services my-service 
kubectl describe services my-service
```

the `external IP address` is shown as <pending> all the time, which is a bug of using `LoadBalancer type service`.

check [git issue 23562](https://github.com/kubernetes/kubernetes/issues/23562), there are three ways to do:

	1) use NodePort instead of LoadBalancer, which will expose it to a port on the cluster IP 

	2) use externalIP option with LoadBalancer service, where the IP can be the host machine's IP ?

for solution 2), add `--external-ip=10.20.180.12`, the externalIP is not pending, but still `curl http://10.20.180.12:8280` doesn't work.


[why loadBalancer service doesn't work](https://stackoverflow.com/questions/44110876/kubernetes-service-external-ip-pending): if you are using a custom Kubernetes Cluster (using minikube, kubeadm or the like). In this case, there is no LoadBalancer integrated (unlike AWS or Google Cloud). With this default setup, you can only use NodePort or an Ingress Controller.

for solution 1), expose the service with `kubectl expose deployment hello-world --type=NodePort --external-ip=10.20.180.12  --name=my-service`, but still can't access the service:

```sh
curl http://10.20.180.12:8280 
curl: (7) Failed to connect to 10.20.180.12 port 8280: Connection refused
```


* cleanup

```sh
kubectl delete services my-service
kubectl delete deployment hello-world
```

**in a word**, this doesn't work well for me. back to Q: how to access k8s service outside the cluster? 



* pods can't be cleaned ?


```sh 
gwm@meng:~/k8s$ kubectl get pods 
NAME                           READY   STATUS        RESTARTS   AGE
hello-world-677ccfbb86-78fkx   0/1     Terminating   17         17h
hello-world-677ccfbb86-svvfs   0/1     Terminating   17         17h
hello-world-677ccfbb86-vlm77   0/1     Terminating   16         17h
```

sol:

```sh
kubectl delete pod <PODNAME> --grace-period=0 --force --namespace <NAMESPACE>
```

the reason maybe due to [command in yaml](https://www.cnblogs.com/gaorong/p/9275795.html)



#### check endpoints


```sh
kubectl get endpoints 
kubectl get svc ? 
```

* endpoints vs externalIP 


[k8s endpoints](https://theithollow.com/2019/02/04/kubernetes-endpoints/)

for services, we could use `labels` to match a frontend service with a backend pod automatically by using a selector. if any new pods had a specific label, the service know how to send traffic to. 




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


* how to change k8s  pods nework cidr, afte initialization ?

	kubeadm init --pod-network-cidr=10.4.0.0/16 --cluster_dns=10.3.0.10 


#### kubectl config 


* [reconfigure a node's kubelet in a live cluster](https://kubernetes.io/docs/tasks/administer-cluster/reconfigure-kubelet/#automatic-rbac-rules-for-node-authorizer)

Basic workflow overview

The basic workflow for configuring a kubelet in a live cluster is as follows:

    Write a YAML or JSON configuration file containing the kubelet’s configuration.
    Wrap this file in a ConfigMap and save it to the Kubernetes control plane.
    Update the kubelet’s corresponding Node object to use this ConfigMap.



Q: what is the API server, how to configure its IP ?


* dump configure file of each node 

```sh
  NODE_NAME="the-name-of-the-node-you-are-reconfiguring"; curl -sSL "http://localhost:8001/api/v1/nodes/${NODE_NAME}/proxy/configz" | jq '.kubeletconfig|.kind="KubeletConfiguration"|.apiVersion="kubelet.config.k8s.io/v1beta1"' > kubelet_configz_${NODE_NAME}
```

in our cluster, we have `ubuntu` and `meng`(as leader) two nodes.

but there is a little difference in their configure:

```sh
<   "clusterDomain": "gwm.l3",
---
>   "clusterDomain": "cluster.local",
40c40
<     "10.3.0.10"
---
>     "10.96.0.10"

```

why always get `error: Missing or incomplete configuration info.  Please point to an existing, complete config file` when running `kubectl` command at working node ? 


[organizing cluster accesss using kubecnfig files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
 

By default, kubectl looks for a file named config in the $HOME/.kube directory








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


## can' access nodePort service outside cluster




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



## understand network policies 


[network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)





## refere

[kubectl cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

[deployments from k8s doc](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

[deploy tiny web server to k8s](https://jekhokie.github.io/k8s/busybox/helm/2020/04/23/small-web-server-to-k8s.html)

[k8s production best practices](https://learnk8s.io/production-best-practices)
















