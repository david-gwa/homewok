
[refer](https://docs.unity3d.com/Manual/UNetOverview.html)

#### high level API(HLAPI)
 HLAPI is a server authoritative system, triggered from  UnityEngine.Networking

#### authority
  host has the authority over all non-player GameObjects;  Player GameObjects are a special case and treated as having "local authority". 


#### local/client authority for npc

method1:  spawn the npc using `NetworkServer.SpawnWithClientAuthority`
method2:  `NetworkIdentity.AssignClientAuthority` 

#### network context properties 
isServer()
isClient()
sLOcalPlayer()
hasAuthority()


#### networked GameObjects

	multiplayer games typically built using Scenes that contain a mix of networked GOs and regular GOs.  networked GOs needs t obe synchronized across all users; non-networked GOs are either static obstacles or GOs don't need to synchronized across players 

	 networked GO is one which has a NetworkIdentiy component. beyond that, you need define what to syncronize. e.g. transform ,variables ..


#### player GO

 NetworkBehavior class has a property: isLocalPlayer, each client player GO.isLocalPlayer == true, and invoke OnStartLOcalPlayer() 

Player GOs represent the player on the server, and has the ability to run comands from the player's client. 


#### spawning GOs
the Network Manager can only spawn and synchronize GOs from registered prefabs, and these prefabs must have a NetworkIdentity component

#### spawning GOs with client authority 

NetworkServer.SpawnWithClientAuthority(go, NetworkConnection), 
for these objects, `hasAuthority` is true on this client and OnStartAuthority() is called on this client.  Spawned with client authority must have `LocalPlayerAuthority` set to `NetworkIdentity`, 


#### state synchronization
[SyncVars] synchronzed from server to client;  if opposite, use [Commands]

the state of SyncVars is applied to GO on clients before `OnStartClient()` called. 


### engine and editor integration

 * `NetworkIdentity` component for networked objects 
 * `NetworkBehaviour` for networked scripts
 * configurable automatic synchronization of object transforms
 * automatic snyc var
 

#### build-in Internet services


#### network visibility 
relates to whether data should or not sent about the GOs to a particulr clinet.

method1:  add Network Proximity Checker component to networked GO
method2:  

#### Scene GOs

 saved as part of a Scene, no runtime spawn



#### actions and communication
method1:  remote actions, call a method across network 
method2:  networking manager/behavior callbacks
method3:  LL network messages 

##### host migration 

host:  a player whose game is acting as a server and a "local client"
remote client: all other players 
so when the host left, host need migrate to one remote client to keep the game alive

how it works:
	enable host migration.  so Unity will distribute the address of all peers to other peers. so when host left,  one peer was selected to be the new host (heart-keeping)


##### network discovery
 	
allow players to find each other on a local area network(LAN)

need component <NetworkDiscovery>,

in server mode, the Network Discovery sends broadcast message over the network o nthe specified port in Inspector;

in client mode, the component listens for broadcast message on the specified port


#### using transport Layer API  (LL API)

socket-based networking








