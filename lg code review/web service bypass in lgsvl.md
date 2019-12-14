
## background 

previously had talked [lg new version code review](), where introduced the new server-browser arch, which is focused on the lgsvl server side implementation, which was based on Nancy and sqliteDB; also a simple introduction about [reactjs]().

the gap how client send a http request to the server is done by `axios`. also another issue is how to access asset resource across domain. namely, running the lgsvl service at one host(192.168.0.10), and http request send from another remote host(192.168.0.13). 


### Axios 

the following is [an example](https://upmostly.com/tutorials/using-axios-with-react-api-requests) on how Axios works. 

```
constructor() {
   this.state = {
     user: null 
   }
 }

componentDidMount() {
  axios.get('https://dog.ceo/api/breeds/image/random')
  .then(response => {
    console.log(response.data);
    if(response.status == 200)
        setState(user, reponse.data)
  })
  .catch(error => {
    console.log(error);
  });
}

 render() {
   return (
  )
 }

```

from React componnet to DOM will call `componentDidMount()`, inside which axios send a GET request to `https://dog.ceo/api/breeds/image/random` for a random dog photo. and can also store the response as this component's state. 



### enact 

[enact](https://enactjs.com/docs/tutorials/setup/) is a React project manager, the common usage: 

```
enact create . # generate project at current dir 
npm run serve 
npm run clean

```

enact prject has a configure file, `package.json`, while can specify the proxy, which is `localhost` by default. if want to bind to a special IP address, this is the right place to modify.

```
        "enact": {
                "theme": "moonstone",
                "proxy": "http://192.168.0.10:5050"
        },

```

inside `lgsvl/webUI`, we need do this proxy configure, to support the across-domain access.


### Nancy authentication

`this.RequiresAuthentication()`, which ensures that an authenticated user is available or it will return HttpStatusCode.Unauthorized. The CurrentUser must not be null and the UserName must not be empty for the user to be considered authenticated. By calling this RequiresAuthentication() method, all requests to this Module must be authenticated. if not authenticated, then the requests will be redirected to `http://account.lgsimulator.com`. You need to include the types in the Nancy.Security namespace in order for these extension methods to be available from inside your module.

this.RequiresAuthentication()  `is equal to` return (this.Context.CurrentUser == null) ? new HtmlResponse(HttpStatusCode.Unauthorized) : null;

all modules in lgsvl web server are authenticated by [Nancy:RequiresAuthentication()](https://github.com/NancyFx/Nancy/wiki/Authentication-overview), for test purpose only, we can bypass this function, and pass the account directly:

```
//  this.RequiresAuthentication();
//  return service.List(filter, offset, count, this.Context.CurrentUser.Identity.Name)
string currentUsername = "test@abc.com";
return service.List(filter, offset, count, currentUsername)

```

in this way, no matter what's the account in React client, server always realize the http request is from the user `test@abc.com`. 


### sqlite db 

in Linux, sqlite `data.db` is stored at `~/.config/unity3d/<company name>/<product name>/data.db`

in Windows, `data.db` is stored at `C:/users/username/AppData/LocalLow/<company name>/<product name>/data.db`

it's interesting when register at lgsvlsimualtor.com, and it actually send the account info back to local db, which give the chance to bypass.



### debug webUI

the chrome and firefox has react-devtools plugins, which helps, but webUI doesn't use it directly. to debug webUI it's even simpler to go to dev mode in browser, and checking the few sections is enough



#### refer

* [bring your data to the front](https://programmingwithmosh.com/javascript/axios-in-react-bring-your-data-to-the-front/)




