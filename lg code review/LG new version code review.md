

# lg new version source code review


the new version [2019.09](https://github.com/lgsvl/simulator) has additionally support for webUI, cloud. which requires additional modules.



## database 

database used `sqlite` project, which is an embedded in-memory db; the ORM used `PetaPoco` project; there are a few db related serices, e.g.  vehicleService, simulationService, which will be used in RESTful web request.

* `DatabaseManager`:

```script 

static IDatabaseBuildConfiguration  DbConfig ;

Init(){

	DbConfig = GetConfig(connectionString)
	using  db =  new SqliteConnection(connectionString){
		db.Open()
}

CreateDefaultDbAssets(){

	using db = Open() 
	if (info.DownloadEnvs != null){
		map =  new MapModel(){url = url  LocalPath=localPath;}
		id =  db.Insert(map)
	}
		
	if (info.DownloadVehicles != null){}

	if(defaultMap.HasValue)
	{
		sim1 = new SimulationModel(){ Cluster=0,  Map=defaultMap.Value,   ApiOnly=false};
		AddSimulation(db, sim1, noBridgeVehicle);
		AddSimulation(db, sim, apolloVehicle);
		db.Insert(simx)
	}
}

AddSimulation(IDatabase db, sim,vehicle){
	conn = new ConnectionModel(){
		simulation = id,
		vehicle = vehicle.Value,
	}
	db.Insert(conn)
}

AddVehicle(db, sim,vehicle){
	conn = new VehicleModel(){
		Url = url ,
	}
	db.Insert(vehicle)
	
	return vehicle.Id;
}

PendingVehicleDownloads(){
	using db=Open(){
		var sql =  Sql.Builder.From("vehicles").Where("status=00", "Downloading");
		return db.Query<VehicleModel>(sql);
	}
}

```

### database ORMs 

using `PetaPoco` to define `ORM` models: 

* users

* sessions 

* maps 

* vehicles 

* clusters

* simulations 

#### PetaPoco 

* Page ->  query a page 

* Single -> query a single item

* Insert()

* Delete()

* Update()


### database provider 

SQLiteDatabaseProvider => GetFactory("Mono.Data.Sqlite.SqliteFactory, Mono.Data.Sqlit")

which is called inside `DatabaseManager::Init()`.

### database services 

*  VehicleService : IVehicleService 

*  MapService 

*  NotificationService =>  NotificationManager.SendNotification()

*  DownloadService =>  DownloadManager.AddDownloadToQueue()

*  ClusterService 

*  SessionService 

*  SimulationService


## Web model

web model is where WebUI server located, which is served by `Nancy` project, in which a new design metholody is applied: Inversin of Control Contaner(IoC), namely `控制反转` in chinese. IoC is used to inject implementation of class, and manage lifecycle,  dependencies.    


web model is the server where talk to webUI through routes, which is defined in the React project.


### Nancy 

used to build HTTP based web service,

* FileStream
* StreamResponse  
* [TinyIoC](https://github.com/grumpydev/TinyIoC)   
* UnityBootstrapper : [DefaultNancyBootstrapper](https://github.com/NancyFx/Nancy/wiki/Bootstrapper), used to automatic discovery of modules, custm model binders, dependencies.


`/Assets/Scripts/Web/Nancy/NancyUnityUtils` 

ConfigureApplicatinContainer(TinyIoCContainer container)
{
  container.Register<UserMapper>();
  container.Register<IMapService>(); 
  container.Register<IClusterService>();
  container.Register<IVehicleService>();
  container.Register<ISimulationService>();
} 


### route modules 

* ClusterModule : NancyModule(service,  userService) : base("clusters") {

	Get("/",  x=>{})
	Get("/{id:long}", x={})
	Post("/", x=>{})
	Put("/{id:long}", x=>{})
	Delete("/{id:long}", x=>{})

}

* SimulationModule : NancyModule()
{
  class SimulationRequest{}
  class SimulationResponse{}
  
  Get("/",  x={})
  Post("/",  x={})
  Put("/{id:long}", x={})
  Post("/{id:long}/start", x={})
  Post("/{id:long}/stop", x={})  
}

e.t.c 


### Config & Loader


* `/Assets/Scripts/Web/Config.cs`: 

used to define `WebHost,  WebPort, ApiHost, CLourUrl, Headless, Sensors, Bridges` e.t.c   


* `Loader.cs` :

```c#

Loader Instance ;    //Loader object is never destroyed, even between scene reloads

Loader.Start(){

	DatabaseManager.Init();
	var config = new HostConfguration{} ;   // ?
	Server = new NancyHost(Config.WebHost);
	Server.Start();
	DownloadManager.Init();
}

Loader.StartAsync(simulation){

	Instance.Actions.Enqueue() =>
	var db = DatabaseManager.Open()
	AssetBundle mapBundle = null; 
		
	simulation.Status "Starting" 
	NotificationManager.SendNotification();
	Instance.LoaderUI.SetLoaderUIState();

	Instance.SimConfig = new SimlationConfig(){
		Clusters, ApiOnly, Headless, Interative, TimeOfDay, UseTraffic...
	}	
}


Loader.SetupScene(simulation){

	var db = DatabaseManager.Open()
	foreach var agentConfig in Instance.SimConfig.Agents:
		var bundlePath = agentConfig.AssetBundle 
		var vehicleBundle = AssetBundle.LoadfromFile(bundlePath)
		var vehicleAssets = vehicleBundle.GetAllAssetNames();
		agentConfig.Prefab = vehicleBundle.LoadAsset<GO>(vehicleAssets[0])
		
	var sim = CreateSimulationManager();	
	Instance.CurrentSimulation = simulation 
} 

```


* `DownloadManager`

	class Download();
	Init(){ client = new WebClient();  ManageDownloads(); }
	


## network module

`network module` is used for communication among master and clients(workers) in the cluster network for cloud support. the P2P network is built on `LiteNetLib` which is a reliable UDP lib. 


### LiteNetLib

[doc](https://documentation.help/LiteNetLib/)

[github](https://github.com/RevenantX/LiteNetLib)


* NetManager 

manager.PollEvents() -> 

* [NetPacketProcessor](https://github.com/RevenantX/LiteNetLib/wiki/NetPacketProcessor-(NetSerializer)-usage), network serializer 


   - Send(peer, command, flag)
   - ReadAllPackets(reader, peer)
   - 


### MasterManager 

### ClientManager 


[configure arguments](https://www.lgsvlsimulator.com/docs/config-and-cmd-line-params/)


