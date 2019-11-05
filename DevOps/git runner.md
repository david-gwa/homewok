
## CI/CD settings

[link](http://10.20.181.119/david/git-page-demo/-/settings/ci_cd)


## install
[11.11](https://docs.gitlab.com/11.11/runner/install/linux-repository.html)


  curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
 apt-cache madison gitlab-runner
 sudo apt-get install gitlab-runner=10.0.0

## error info
ERROR: Registering runner... failed                 runner=wcYDvAxB status=500 Internal Server Error
PANIC: Failed to register this runner. Perhaps you are having network problems 


gitlab version  //10.20.181/119  --> 12.1.4

gitlab-runner version   12.1.0 -->  


* try 12.1.0(master)  register failed 
* try  10.0.0, register failed
* try  11.1.0, register failed
* try 10.8.0, register failed
* try 12.0.1



## gitlab.runner  vs  gitlab-ci-multi-runner 

[link](https://www.cnblogs.com/cnundefined/p/7095368.html)


## check runner config info


```shell

gitlab-runner list 

``` 

can't get gitlab-runner work,  



### config gitlab.rb first 

[config](https://www.liangzl.com/get-article-detail-126717.html)


/opt/gitlab/embedded/cookbooks/cache/cookbooks/gitlab/libraries/gitlab_pages.rb 

Gitlab['gitlab_pages']['artifacts_server_url'] ||=  Gitlab['external_url'].chomp('/') + '/api/v4'


[gitlab pages https service with dns](https://blog.csdn.net/mehnr/article/details/85064116)




config gitlab.yml file:

```shell
	pages:
	artifacts_server:  true -> false 

```


### gitlab server and gitlab page server with same IP



### apache web server 

[install apache](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-16-04)

[configure apache](https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps)

[start apache](https://phoenixnap.com/kb/ubuntu-start-stop-restart-apache)

[host static website](https://www.raspberrypi.org/magpi/apache-web-server/)


	

