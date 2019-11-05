

## background 

during ADS development, ros bag is used a lot to record the sensor, CAN and scenario info, which helps in vehicle test, data fusion, perception.
[cruise webviz](https://github.com/cruise-automation/webviz) is an open source tool to visualize rosbag and allow user defined layout in web environment, without the pain to run `roscore` and other ros nodes.

while js is not a common tool in my visibility, the way how an js project is organized is really confused at the first time. there are a punch of new things:

* [react](https://create-react-app.dev/)
* [regl]https://www.giacomodebidda.com/how-to-get-started-with-regl-and-webpack/)


and `js` functions/modules are really patches, they can be pached anywhere in the project, so usually it requires a patch manager(e.g. lerna) to deal with versions, dependencies etc; and bigger there are packages, which is independent function component.

webviz has a few packages, e.g. regl-worldview, webviz-core, which has more than 40 patches(modules) used.

* [cruise:worldview](https://webviz.io/worldview/#/docs/tutorial/introduction)

* [cruise:webviz core]()

* [rosbag.js](https://github.com/cruise-automation/rosbag.js)


## lerna

[lerna](https://github.com/lerna/lerna) is an open source tool to manage js project with multi packages.

* `lerna init` will generate `lerna.json`, which defines the required modules

* `package.json` defines useful infomation about the module depencies,  CLI(which give a detail about how things work behind) and project description

* `lerna bootstrap --hoist react` will install all required modules in the root folder `/node_modules`, if doesn't work well, leading to `Can't Resovle module errors`,  may need manually install some.


## webpack 

[webpack](https://webpack.js.org/guides/getting-started/) is an open source tool for js module bundler. 

`webpack.config.js`, defines `entry`, where the compiler start; `output` , where the compiler end; `module`, how to deal with each module; `plugin`, additionaly content post compiliation; `resovle.alias` define alias for modules.


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


the JS bundle could be loaded from a static HTML page, served with any simple web server. That's exactly what this /packages/webviz-core/public/index.html file is, which is used for https://webviz.io/try. The webpack dev server is configured to serve it at /webpack.config.js


## npm commands 

```script 

npm config list 
npm install packages@version.minor [-g] [--save]
npm uninstall packages 
npm search packages
npm cache clean --force 

 
```


## webpack-server 

[webpack-server](https://github.com/webpack/docs/wiki/webpack-dev-server) is a little nodejs Express server. to install it as a CLI tool first, then run it under the webviz project root folder, with optional parameters, e.g.  --host, --port e.t.c



## webviz configure 

* npm config set registry https://r.npm.taobao.org
* npm install puppeteer --unsafe-perm=true
* npm run bootstrap

if failed: 
* sudo npm cache  clean --force 
* npm install -g lerna 
* npm run bootstrap 	
* sudo npm install/rebuild node-sass 
* npm run build

if failed, manually installed unresovled modules
* npm test   

if failed based on a few test modules, install then
* npm install  webpack-dev-server --save 

webpack-dev-server.js --host IP --port 8085  #under project root


a little hack, by default `npm install inter-ui` [phli's inter-ui](https://github.com/philipbelesky/inter-ui/tree/master/Inter%20(web)), where inside
`webviz/packages/webvix-core/src/styles/fonts.module.scess`, it uses: `url("~inter-ui/Inter UI (web)/Inter-UI.var.woff2") format("woff2-variations")`, modified this line to: `url("~inter-ui/Inter (web)/Inter.var.woff2") format("woff2-variations")`
 

## refer

[tabbles](https://tabbles.net/)

[webviz in ros community](https://discourse.ros.org/t/webviz-ros-data-visualization-in-the-browser/9783)

[access web-server in LAN](https://stackoverflow.com/questions/33272967/how-to-make-the-webpack-dev-server-run-on-port-80-and-on-0-0-0-0-to-make-it-publ)

[issue: how to run cruise webviz](https://github.com/cruise-automation/webviz/issues/161)

[Ternaris Marv](https://ternaris.com/marv-robotics/)
 
[minio: high performance object storage for AI](https://min.io/)

[webviz on remote bag](https://github.com/cruise-automation/webviz/issues/247)

[visuaize data from a live server](https://github.com/cruise-automation/webviz/issues/118)

[npm package install in China](https://stackoverflow.com/questions/22764407/npm-install-goes-to-dead-in-china)

[taobao.npm](https://npm.taobao.org/package/cnpm)




