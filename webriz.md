
## prepare

```shell

apt-get install npm

npm install -g n #n is nodejs manager 

n #will install nodejs

```

if download failed, find nodejs src from [aliyun](https://npm.taobao.org/mirrors/node/v10.16.2/) and [install nodejs from src](https://www.techaroha.com/install-node-js-source-code/)


## install webviz 

```shell

npm run build



``` 


* error unable to run lerna, [sol](https://stackoverflow.com/questions/50522215/unable-to-run-lernas-command)


```shell
cd  /path/to/node/install/file 

sudo npm init -f 

sudo npm install lerna 

```

[lerna error1](https://blog.csdn.net/li11_/article/details/87452242)



## webviz 

[install](https://github.com/cruise-automation/webviz#developing)


> npm install && lerna bootstrap --hoist react

npm ERR! code ETIMEDOUT
npm ERR! errno ETIMEDOUT
npm ERR! network request to https://registry.npmjs.org/enzyme-adapter-react-16/-/enzyme-adapter-react-16-1.11.2.tgz failed, reason: connect ETIMEDOUT 104.16.24.35:443
npm ERR! network This is a problem related to network connectivity.
npm ERR! network In most cases you are behind a proxy or have bad network settings.
npm ERR! network 
npm ERR! network If you are behind a proxy, please make sure that the
npm ERR! network 'proxy' config is set properly.  See: 'npm help config'

 

[solution](https://www.jianshu.com/p/d69b1d8bc2a6)

```shell
npm config set registry http://registry.cnpmjs.org
npm info underscore 
npm install -g cnpm --registry=https://registry.npm.taobao.org
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1
npm i puppeteer

``` 

> puppeteer@1.19.0 install /home/wubantu/zj/webviz/node_modules/puppeteer
> node install.js

ERROR: Failed to download Chromium r674921! Set "PUPPETEER_SKIP_CHROMIUM_DOWNLOAD" env variable to skip download.
{ Error: EACCES: permission denied, mkdir '/home/wubantu/zj/webviz/node_modules/puppeteer/.local-chromium'
  -- ASYNC --


[solution](https://www.jianshu.com/p/d69b1d8bc2a6)





* [unsafe-perm](https://stackoverflow.com/questions/48869749/npm-install-puppeteer-showing-permission-denied-errors)

sudo rm -rf node_modules

npm install 


follow  [cruise install](https://github.com/cruise-automation/webviz#developing)

* Error: ENOENT: no such file or directory, scandir '/home/wubantu/zj/webviz/node_modules/node-sass/vendor'

[solution](https://github.com/sass/node-sass/issues/1579)



* npm rebuild node-sass error
[solution](https://github.com/nodejs/node-gyp/issues/1133)
[sol2](https://github.com/nodejs/node-gyp/issues/1020)



 
summary :

```shell
sudo -i  #as root
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1 
npm install puppeteer --unsafe-perm=true
npm run bootstrap
sudo npm rebuild node-sass 
npm run build
npm test
```


















## cruise developer talk

[cruise webviz](https://discourse.ros.org/t/webviz-ros-data-visualization-in-the-browser/9783)


## introduction of Cruise 

[cruise github](https://github.com/cruise-automation)


