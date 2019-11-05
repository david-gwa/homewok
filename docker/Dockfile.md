

[Dockerfile Doc](https://docs.docker.com/engine/reference/builder/)

#### Format

	#comment
	INSTRUCTION  arguments 

e.g.
	#echo demo
	RUN echo 'running echo'


#### FROM

 	FROM <image>:[<tag>]  [AS <name>]

	
#### RUN
	RUN <command>

the command run in shell, /bin/sh -c in Linux by default	
`\`(backslah) can used to continue a single RUN instruction onto the next line

to run non-default shell, parsing as a JSON array, which means you should use `"`(double-quotes)
	 RUN ["/bin/bash", "-c", "echo hello"]


#### CMD
	CMD ["executable", "param1", "param2"]
or
	CMD ["param1", "param2"]  (as default parameters to ENTRYPOINT)
or
	CMD command param1 param2 


there suppose only one `CMD` in one Dockfile, `CMD` provides defaults for an executing container



#### ADD

	ADD [--chown=<user>:<group>] <src> ... <dest>
or 
	ADD ["<src>", ... "<dest>"]	

`ADD` copy files from `<src>` to current filesystem of the image at `<dest>`

`<src>` is relative to the source of the context of the build 

`<dest>` is an absolute path, or a path relative to `WORKDIR`


#### EXPOSE
	EXPOSE <port>  [<port>/<protocol> ...]

the container listens on the specified network ports at runtime. by default the ports listen on TCP 

#### WORKDIR
	WORKDIR /path/to/workdir
	
`WORKDIR` set the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, `ADD` instructions that follow it

#### COPY

	COPY [--chown=<user>:<group>] <src> ... <dest>

or 
	COPY [--chown=<user>:<group>] ["<src>".  ... "<dest>"]

similar as `ADD`


#### ENTRYPOINT

	ENTRYPOINT ["executable", "param1", "param2"] 
or 
	ENTRYPOINT command param1 param2 


this is the starting point when executing this image. the `docker run` parameters can override the parameters in `ENTRYPOINT`


#### how CMD and ENTRYPOINT interact 

`CMD` used to define default arguments for an `ENTRYPOINT` command or for executing an ad-hoc command in a container, and it can be overridden by arguments passing in `docker run`

`ENTRYPOINT` should be defined when using the container as an executable





