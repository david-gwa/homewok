


## what is React 

used to build complex UI from small and isolated pieces of code "components" 

```js 

class vehicleManager extends React.Component {
	render()
	{
		return <html></html>
	} 
}

```

React will render the html on screen, and any changes in data, will update and rerender. 


`render()` returns a description(React element) of what you want to see on the screen, React takes the descriptions and displays the result.  

### passing data through props 

### making an interactive component


## npm tool

```shell

npm search

npm install [-g] 

npm remove 

npm pack 

npm view 

```


### node_module path

global node_modules path ?

### package.json


### build a react hello-world app

```shell
npx create-react-app react-demo

cd react-demo
```

output: 

```

Initialized a git repository.

Success! Created react-demo at /home/wubantu/zj/react-in/react-demo
Inside that directory, you can run several commands:

  npm start
    Starts the development server.

  npm run build
    Bundles the app into static files for production.

  npm test
    Starts the test runner.

  npm run eject
    Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!

We suggest that you begin by typing:

  cd react-demo
  npm start

Happy hacking!

```

error report: 


events.js:174
      throw er; // Unhandled 'error' event
      ^

Error: ENOSPC: System limit for number of file watchers reached


this error is due to opened too many files, close a few VScode project is the solution


### JSX intro

### element rendering 

### components 

components works as a func, and props is the func's paramters, the func will return a React element which rendered in view


### props and state 's lifecycle

一个React组件的生命周期分为三个部分：实例化、存在期和销毁时。

  initial render -> constructor() -> componentWillAmunt() -> render() -> componentDidMount() --> componentWillUnmount() 


### event handler and bind()


## react app structure


* components/ ,  e.g.  NavBar, Button, CheckBox, PageHeader, MapManager, SimulationManager, VehicleManager

* views/ ,   dashboard, login

* App/



###  App.js vs index.js 

[from stackoverflow](https://stackoverflow.com/questions/50493069/why-does-create-react-app-creates-both-app-js-and-index-js)

[refer 2](https://stackoverflow.com/questions/21063587/what-is-index-js-used-for-in-node-js-projects)

`index.js` is the traditional and actual entry point for all Node apps. in React, it tells what to render and where to render.  

in general, web server looks for certain files to load first, namely `index.js` 

`App.js` has the root component of React app,  every view and component are handles iwth hierarchy in React, <App /> is the top most component in the hierarchy. 

[react in chinese](https://reactjs.org.cn/doc/hello-world.html)
 

###  React.createContext

[understand context jianshu](https://www.jianshu.com/p/eba2b76b290b)

[front-end zhihu](https://zhuanlan.zhihu.com/p/42654080)

* what is context ?
In Some Cases, you want to pass data through the component tree without having to pass the props down manuallys at every level. you can do this directly in React with the powerful "context" API.

使用props或者state传递数据，数据自顶下流。 (<App> -->  <Node> -->  <SubNode> --> <Child> ) 
使用Context，可以跨越组件进行数据传递。

```js
const SimulationContext = React.createContext({
		simulaitonEvents: null,   //default value
		mapDownloadEvents: null,
		simulation: {}
	})

```
[创建一个 Context 对象](https://react.docschina.org/docs/context.html#reactcreatecontext)。当 React 渲染一个订阅了这个 Context 对象的组件，这个组件会从组件树中离自身最近的那个匹配的 Provider 中读取到当前的 context 值。
只有当组件所处的树中没有匹配到 Provider 时，其 defaultValue 参数才会生效。这有助于在不使用 Provider 包装组件的情况下对组件进行测试。注意：将 undefined 传递给 Provider 时，消费组件的 defaultValue 不会生效


* Provider, usually in Parent node

每个 Context 对象都会返回一个 Provider React 组件，它允许消费组件订阅 context 的变化。

Provider 接收一个 value 属性，传递给消费组件。一个 Provider 可以和多个消费组件有对应关系。多个 Provider 也可以嵌套使用，里层的会覆盖外层的数据。

当 Provider 的 value 值发生变化时，它内部的所有消费组件都会重新渲染。


SimulationProvider, used in Home.js

* Consumer, usually define one or multi in childre node


###  this.setState


[setState](http://huziketang.mangojuice.top/books/react/lesson10) 方法由父类 Component 所提供。当我们调用这个函数的时候，React.js 会更新组件的状态 state ，并且重新调用 render 方法，然后再把 render 方法所渲染的最新的内容显示到页面上
当我们要改变组件的状态的时候，不能直接用 this.state = xxx 这种方式来修改，如果这样做 React.js 就没办法知道你修改了组件的状态，它也就没有办法更新页面。所以，一定要使用 React.js 提供的 setState 方法，它接受一个对象或者函数作为参数。

### promise.then()


### EventSource

server to client pushing one-way only, EventSource只能发送文本

event： 事件类型，如果指定了该字段，则在客户端接收到该条消息时，会在当前的EventSource对象上触发一个事件，事件类型就是该字段的字段值，你可以使用addEventListener()方法在当前EventSource对象上监听任意类型的命名事件，如果该条消息没有event字段，则会触发onmessage属性上的事件处理函数。


[eventsource vs websocket](https://juejin.im/post/5c121c77f265da614a3a5e07)

[broswer and server eventSource](https://www.cnblogs.com/accordion/p/7764460.html)

* broswer side

`var eventSource = new EventSouce("/events")  #/events is data provider from server`
默认EventSource对象通过侦听“message”事件获取服务端传来的消息
EventSource规范允许服务端指定自定义事件，客户端侦听该事件即可。
`eventSource.addEvenListener('VehicleDownload', (e)=>this.handleVehEvents(e));`


* server side 
服务端返回数据需要特殊的格式，它分为四种消息类型： event, data, id, retry
event指定自定义消息的名称，如event: customMessage\n;


### react-router-dom :: Route

[in chinese](https://www.jianshu.com/p/97e4af32811a)


<Route path=, component= />
<Route render={ths.routeRender} />



### useState, useContext, useCallback, useEffect

[in chinese](https://www.jianshu.com/p/e61faf452565)


* [function component](https://github.com/xiaohesong/TIL/blob/master/front-end/react/hooks/state-hook.md) vs  class component

as funciton component has no `this.state`, so `Hook` is the way to add `React state` to function component. when function component exit, in common the state disappear/cleared, but `Hook` help to keey this state. 

* intial hook

the only parameter pass in hook::useState(new Map()) is  the initial state.   useState(initState)

* return from useState

it returns a pair [currentState, setStatefunc], e.g.  [maps, setMaps],  setStatefunc here is similar as `this.setState` in class component


* access state

directly  {currentState}

* update state

{() => setStatefunc(currentState)} 


 

## react route base



### js arrow function



## from Nancy to React 

/Assets/Scripts/Web/Modules/*Moduele.cs  Get["/xx"]  --->

/WebUI/src/APIs.js  axios.put["/xx"]





## refer

[reactjs.org/tutorial](https://reactjs.org/tutorial/tutorial.html)




















