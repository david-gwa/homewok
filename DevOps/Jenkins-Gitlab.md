

## background 

after built the Gitlab server in LAN for two month, managing about 20 projects in ADS group currently. the needs for CI is coming up. at very beginning, I tried Gitlab CI runner, doesn't work through. so Jenkins!


## Jenkins installation

there is a great series [Maxfields jekins-docker tutorial](https://github.com/maxfields2000/dockerjenkins_tutorial), since originally I had Docker env and which is a prepartion for cloud deployment in future.

* [Jenkins in Docker installation](https://jenkins.io/doc/book/installing/#debian-ubuntu), 

* start Jenkins in Docker

```shell
docker run --rm -p 8080:8080 -p 50000:50000 -v jenkins-data:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock  jenkinsci/blueocean 

```

* [setup wizard](https://jenkins.io/doc/book/installing/#setup-wizard)


also Jenkins installed directly in [Ubuntu](https://linuxize.com/post/how-to-install-jenkins-on-ubuntu-18-04/)


## Jenkins integrated with Gitlab

Jenkins default has integrated with BitBucket and Github, to integrate with Gitlab:


* set Gitlab token

in Gitlab Project main page, go to `User Profile` >> `Settings` >> `Peronsal Access Token`, naming the token and click `api` domain, the token is generated. 


* install Gitlab Plugins   

in Jenkins main page: `Manage Jenkins` >> `Manage Plugins` >> Search Available Plugins (gitlab).


* add gitlab key credentials 

in Jenkins main page, go to `Credentials`, choose the key type to `Gitlab API token`, then generate the key credential, used to access Gitlab project. 

* configure Jenkins with gitlab

in Jenkins main page, go to `Manage Jenkins` >> `Configure System`, at the gitlab section, add the gitlab host url and use the credential created at previous step.

since the gitlab server is hosted in LAN, even don't have DNS for the gitlab server, purely raw IP address. so the gitlab host URL is like:

	http://10.20.110.110:80 

rather than the project git url (e.g.  http://10.20.110.110/your_name/your_project.git)



## Gitlab Hook Plugin

gitlab events will be post to Jenkins through webhook, which is a common way to notify external serivces, e.g. dingding office chat, JIRA e.t.c. To set it up, need to configure `Gitlab Hook` plugin in Jenkins.

as mentioned in [this post](https://linuxize.com/post/how-to-install-jenkins-on-ubuntu-18-04/), JDK10 or 11 is not supported  for Jenkins, if the current OS system has already JDK11, need addtionally install jdk8, and configure the default jdk=8: 

```shell

update-java-alternatives --list 

sudo update-alternatives --config java 

java -version

```

## Jenkins Project 

add a new Jenkins Item, select `FreeStyle`, go to `Configure`.

in `Source Code Management` section, select `Git`. add Repository URL and set gitlab username and password as Jenkins Credentials. 

in `Build Triggers` section, select `Build when a change is pushed to Gitlab`, which display the Gitlab webhook URL: http://localhost:8080/jenkins/project/demo; go to `Adavance` section to generate the secret token.


when getting all these done, back to Gitlab project, as Admin or Maintainer, in Project `Settings` >> `Integrations` >> `Add Webhooks`.URL and Secret Token are from the previous settings.

there is a common issue: **Url is blocked: Requests to localhost are not allowed**, please refer to [allow request to localhost network from system hooks](https://docs.gitlab.com/ee/security/webhooks.html)





## refer

[riot games: putting jenkins in docker](https://technology.riotgames.com/news/putting-jenkins-docker-container)

[jenkins to gitlab authentication](https://github.com/jenkinsci/gitlab-plugin#jenkins-to-gitlab-authentication)

[devops expert: Emil](https://emilwypych.com/emil-wypych/)

[mind the product: PM's guide to CD & DevOps](https://www.mindtheproduct.com/what-the-hell-are-ci-cd-and-devops-a-cheatsheet-for-the-rest-of-us/)
[manage multi version of JDK on Ubuntu](https://www.oodlestechnologies.com/blogs/Managing-Multiple-version-of-JDK-on-Ubuntu/)



[a jianshu refer](https://www.jianshu.com/p/7dd79e6c0ac5)

[a aliyun refer](https://yq.aliyun.com/articles/659876)

[tencent refer](https://cloud.tencent.com/developer/article/1465854)

[allow request to localhost network from system hooks](https://docs.gitlab.com/ee/security/webhooks.html)




