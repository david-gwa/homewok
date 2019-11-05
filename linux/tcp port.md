### netstate 详解
https://blog.csdn.net/Linux_ever/article/details/50775292



(base) ubuntu@ubuntu:/etc$ netstat -lat 
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 localhost:http-alt      *:*                     LISTEN     
tcp        0      0 127.0.1.1:domain        *:*                     LISTEN     
tcp        0      0 *:ssh                   *:*                     LISTEN     
tcp        0      0 localhost:ipp           *:*                     LISTEN     
tcp        0      0 *:microsoft-ds          *:*                     LISTEN     
tcp        0      0 *:netbios-ssn           *:*                     LISTEN     
tcp        0      0 bdjs-4cv919wmwk.t:37134 104.18.124.25:https     ESTABLISHED
tcp        0      0 bdjs-4cv919wmwk.t:48612 121.17.123.141:https    TIME_WAIT  
tcp        0      0 bdjs-4cv919wmwk.t:39122 104.18.122.25:https     ESTABLISHED
tcp        0      0 bdjs-4cv919wmwk.t:37490 218.11.0.86:https       TIME_WAIT  
tcp        0      0 bdjs-4cv919wmwk.t:44790 lb-192-30-253-124:https ESTABLISHED
tcp        0      0 bdjs-4cv919wmwk.t:59584 119.249.49.122:https    TIME_WAIT  
tcp        0      0 192.168.0.1:41022       192.168.0.2:2377        ESTABLISHED
tcp        0      0 bdjs-4cv919wmwk.t:57174 104.18.125.25:https     ESTABLISHED
tcp        0      0 bdjs-4cv919wmwk.t:44988 ec2-52-43-6-175.u:https ESTABLISHED
tcp        0      0 172.17.0.1:netbios-ssn  bdjs-4cv919wmwk.t:54020 ESTABLISHED
tcp       12      0 172.17.0.1:54020        172.17.0.1:netbios-ssn  ESTABLISHED
tcp        0      0 bdjs-4cv919wmwk.t:37482 218.11.0.86:https       ESTABLISHED
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN     
tcp6       0      0 ip6-localhost:ipp       [::]:*                  LISTEN     
tcp6       0      0 [::]:microsoft-ds       [::]:*                  LISTEN     
tcp6       0      0 [::]:2376               [::]:*                  LISTEN     
tcp6       0      0 [::]:2377               [::]:*                  LISTEN     
tcp6       0      0 [::]:7946               [::]:*                  LISTEN     
tcp6       0      0 [::]:netbios-ssn        [::]:*                  LISTEN     
tcp6       0      0 192.168.0.1:7946        192.168.0.2:51220       TIME_WAIT  
tcp6       0      0 192.168.0.1:7946        192.168.0.2:51224       TIME_WAIT  
tcp6       0      0 192.168.0.1:2377        192.168.0.2:58416       ESTABLISHED



#### 172.17.0.1

Docker0 default value 



### udp 丢包

netstat -us



