
## directly run web binary?

[check nvidia card]

```shell
 lspci -vnn  | grep VGA -A 12 

```
Qudaro p2000 

## upgrate gpu driver 
[link](https://websiteforstudents.com/install-proprietary-nvidia-gpu-drivers-on-ubuntu-16-04-17-10-18-04/)

[nvidia-390 driver download](https://www.nvidia.com/Download/driverResults.aspx/149145/en-us)

can't install nvidia-390 successfully. 


## install vulkan

[vulkan support gpu](https://developer.nvidia.com/vulkan-driver)
Latest Legacy GPU version (390.xx series): 390.129
Latest Legacy GPU version (340.xx series): 340.107

[Ubuntu driver version]

Error: You appear to be running an X server; 


ctrl + alt + F1 

sudo service lightdm stop or sudo lightdm stop
sudo init 3
sudo service lightdm start

nvidia distribution provided preinstall script has failed 


try to install `nvidia-390`, which failed....

directly install  `sudo apt-get install libvulkan1` with current existing `nvidia-384`:





## install enact 

[link](https://github.com/enactjs/cli)

npm install @enact/cli


## how npm run works ?

[liao](http://www.ruanyifeng.com/blog/2016/10/npm_scripts.html)


## npm run serve


Proxy error: Could not proxy request /users from localhost:8088 to http://localhost:8080.
See https://nodejs.org/api/errors.html#errors_common_system_errors for more information (ECONNREFUSED).

Proxy error: Could not proxy request /favicon.ico from localhost:8088 to http://localhost:8080.
See https://nodejs.org/api/errors.html#errors_common_system_errors for more information (ECONNRESET).

Proxy error: Could not proxy request /sockjs-node/179/5v0tekkb/websocket from localhost:8088 to http://localhost:8080.


sol: 

make sure the proxy port defined in `package.json` at `script` and `enact` are same. here using `8088`



## React introduction


#### simulator build webui

previously, install nodejs,npm.

in c#   new Process() ->  to [call external apps](https://www.cnblogs.com/tianma3798/p/6016130.html)

#### open browser

Application.OpenURL(Loader.Instance.Address + "/")



### Nancy 

[nancy](http://nancyfx.org/)

[doc](https://github.com/NancyFx/Nancy/wiki/Documentation)


[Nancy hello-world](http://yimingzhi.net/2015/04/nancyfx-xi-lie-zhi-hello-world): 

```shell
Get["/"] = p => {
    var model = SomeModel();
    return model;
};

```

* content negotiation 

end-user in browser(view layer) wnat to access `/` path, then Nancy find the view corresponding to `model` and send back `model` data to this view.

if request a json data from `view layer`, then the send-back `model` is a serialized data, rather than a html

构造函数中定义路由地址和请求方式，Get["/"]表示通过GET方式请求"/"地址。
nancy 只是一种响应http请求的服务端框架，


## Model-View-Controller 


### PetaPoco 

light-weight ORM(object relational mapper) framework [doc](https://github.com/CollaboratingPlatypus/PetaPoco)


### SQLite


## LoaderUI

### loader

```c#
SetupScene(simulationModel simulation){

	#add vehicle
	vehicleBundle = AssetBundle.LoadFromFile()
	vehilceAssets = vehicleBundle.getAssets()
	prefab = vehicleBundle.LoadAsset<GO>(vehicleAssets)
	agent = new AgentConfig(){Prefab = prefab)
	agents.Add(agent)
	vehicleBundle.Unload()
	#instance simulationManager 
	sim = Instantiate(Instance.SimulatorManagerPrefab)
	# notify webUI simulation is running
	NotificationManager.SendNotification("simulation", SimulationResponse.Create(simulation)


class NotificationManager{
	JavaScriptSerializer Serializer ;
	SendNOtification(string @event, object obj): 
		Message(){Event = event, Data=Serializer.Serialize(obj)


class SimulationResponse{
	Create(SimulationModel simulation)
	{
			
	}
	
```

* JavaScriptSerializer used to serialize and deserialize JSON


## databasemodels 

* SimulationModel


### IndexModule




###  c# 匿名函数 & 委托 & enclose &  lambda 表达式 & 内联

[link](https://docs.microsoft.com/zh-cn/dotnet/csharp/programming-guide/statements-expressions-operators/anonymous-functions)


* expression lambda: 

```shell
(input-parameters) => expression
```

* sentence lambda: 

```shell
(input-parameters) => { <sequence-of-statements> }
```


* assign lambda expression to a variable/handler ?



### nancy modules 

[refere doc](http://liulixiang1988.github.io/nancy-webkuang-jia.html#_1)
模块能够在全局被发现
使用模块为路由创建一个根

* 定义路由
HTTP方法(GET/POST...)+模式(/some/{thing}/)+动作(lambda sentence)+(可选)条件

* 选择路由
一个请求有时符合多个模式，此时记住： 1. module的顺序在启动时不定 2. 同一module中的路由是按顺序来的 3. 多个匹配中，得分最高的匹配 4. 得分相同的匹配按照启动时的顺序匹配


* 模型绑定
Nancy.ModelBinding
used in  /Web/Modules/xxModule.cs 

* bootstrapper 
bootstrapper负责自动发现模型、自定义模型绑定、依赖等等。可以被替换掉。


* view engine 
视图引擎就是输入“模板”和“模型”，输出HTML（大部分情况下）到浏览器。




## nancy app

[meet nancy](https://auth0.com/blog/meet-nancy-a-lightweight-web-framework-for-dot-net/)

first, app trigger nancyhost.start(), then add a router module, any time when the router is triggered, it will get data returned from nancy.

the router module: In just the same way you might include a NuGet package or third-party library, you are creating functionality in program code that can be called from other applications across a network link. 


* create a NancyHost 
* add a NancyModule route

## how Nancy talk with front-end in js



## Axios 

[official doc](https://www.kancloud.cn/yunye/axios/234845)




## webpack
[webpackjs](https://www.webpackjs.com/)

Webpack 是一个前端资源加载/打包工具
Webpack会帮助我们生成dist目录


modules with dependencies -->   static assets 

 
#### [webpack concept](https://www.webpackjs.com/concepts/)

* entry, let webpack which module to start 

## build back-end for react 
[link](https://www.jianshu.com/p/c0ba97f2b6a1)

#### folder structure 

* src/api # interface
* src/components # react components 
* src/router # 
* src/views  # to store webpages 


#### define page and related components 

* APP.js,  HOME.js,  Loading.js all extends  `React.Component` 

APP will route to home page or loading page, based on state.user != null 

#### build router based on page 

in HOME.js  <Route path="/vehicles" component={this.VehicleManager} />
in LOADING.js  plain html


#### route trigger in index.js 

 `render(appElement, document.getElementById('root'))` ->  向页面返回了一个路由组件,  namely:   localhost:8080/#/


#### components in HOME.js














