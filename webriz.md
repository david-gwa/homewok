
## prepare

```shell

apt-get install npm

npm install -g n #n is nodejs manager 

```

install nodejs (node-v10.16.2.tar.gz) from src 



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
npm install  webpack-dev-server
./node_modules/webpack-dev-server/bin/webpack-dev-server.js --host 10.20.181.132 --port 838
```

## a webpack app structure 

[webpack](https://webpack.js.org/guides/getting-started/)

webpack-demo
|- package.json
|- webpack.config.js
|- /dist
  |- main.js
  |- index.html
|- /src
  |- index.js
|- /node_modules




## how to run 

`npm run build` to compile the package with webpack, so it can be run with node

the JS bundle could be loaded from a static HTML page, served with any simple web server. (That's exactly what this /packages/webviz-core/public/index.html file is, which is used for https://webviz.io/try. The webpack dev server is configured to serve it at /webpack.config.js) 

[how to run](https://github.com/cruise-automation/webviz/issues/161)


## set webpack.config

[config](https://stackoverflow.com/questions/33272967/how-to-make-the-webpack-dev-server-run-on-port-80-and-on-0-0-0-0-to-make-it-publ)




## where to set localhost:port 

node_modules/react-modal/package.json:    "start": "webpack-dev-server --inline --host 127.0.0.1 --content-base examples/",

node_modules/react-treebeard/example/webpack.config.js:        'webpack-dev-server/client?http://0.0.0.0:8080',



[fix links to webviz tool](https://github.com/cruise-automation/webviz/pull/160/commits/119ac1234efa0d2efe5df1e5c00c4693362c474b)


[how to run webviz locally](https://github.com/cruise-automation/webviz/pull/160/commits/625465b358ba8d155aa0f311cbe10a4f35400580)



## add html to another html

[link1](https://stackoverflow.com/questions/8988855/include-another-html-file-in-a-html-file)



## how  npm run cowork with webpack-dev-server



## cruise developer talk

[cruise webviz](https://discourse.ros.org/t/webviz-ros-data-visualization-in-the-browser/9783)


## introduction of Cruise 

[cruise github](https://github.com/cruise-automation)



## webpack-dev-server

a light-weight Node.js Express server

[webpack](https://segmentfault.com/a/1190000006964335)

[webpack on 0.0.0.0](https://stackoverflow.com/questions/33272967/how-to-make-the-webpack-dev-server-run-on-port-80-and-on-0-0-0-0-to-make-it-publ)



```python

var path=require("path")

module.exports ={
	entry: { app:["./app/main.js"] }
     	output: {path: path.resolve(__dirname, "build")} 
}


npm install webpack-dev-server

npm list | head -n 1 

webpack-dev-server --inline --hot

```

## npm run build product-deploy

[npm run build packages](https://blog.csdn.net/luckyzsion/article/details/80251810)

then  nginx configure run env

[nginx withe nodejs](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-node-js-application-for-production-on-ubuntu-14-04)


## webpack config a nodejs app

host by local IP


## multi package.json project 

## webpack build and run ?


./node_modules/webpack-dev-server/bin/webpack-dev-server.js --host 10.20.181.132 --port 838




