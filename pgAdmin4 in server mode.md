## pgSQLServer 

* [official install postgresql](https://www.postgresql.org/download/linux/ubuntu/)

* [start pgSQLserver](https://www.postgresql.org/docs/current/server-start.html)

* jump into pgSQL server:

	/etc/init.d/postgresql start 

	sudo su - postgres 


## pgAdmin4 

installed by `apt-get install pgadmin4`, will put pgAdmin4 under local user or root permission, which will be rejected if accessed by remote clients. 

so it's better to install from src and in a different Python virtual env.

* [setup Python virtual Env](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-18-04-server)

* [install pgAdmin4 from src](https://www.digitalocean.com/community/tutorials/how-to-install-configure-pgadmin4-server-mode)

there maybe a few errors as following:

     *  No package 'libffi' found  
      
     *  error: invalid command 'bdist_wheel' [sol](https://stackoverflow.com/questions/34819221/why-is-python-setup-py-saying-invalid-command-bdist-wheel-on-travis-ci)

     * error: command 'x86_64-linux-gnu-gcc' failed with exit status 1, [sol](https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory)


## configure pgAdmin4

follow [this configure pgadmin4 in Server mode](https://www.digitalocean.com/community/tutorials/how-to-install-configure-pgadmin4-server-mode)


## configure Apache2 

follow previous blog to set Apache2 for pgadmin4:

```script 
<VirtualHost *:8084>
    ServerName 10.20.181.119:8084
    ErrorLog  "/var/www/pgadmin4/logs/error.log"
    WSGIDaemonProcess pgadmin  python-home=/home/david/py_venv/pgenv
    WSGIScriptAlias /pgadmin4 /home/david/py_venv/pgenv/lib/python3.5/site-packages/pgadmin4/pgAdmin4.wsgi

    <Directory "/home/david/py_venv/pgenv/lib/python3.5/site-packages/pgadmin4/">
        WSGIProcessGroup pgadmin
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>

``` 

restart Apache2 server will make this works.


in summary: so far we can host pgAdmin4 in Apache web server, which is a good support for team work in same LAN. 


## refer 

[why sudo - su](https://serverfault.com/questions/601140/whats-the-difference-between-sudo-su-postgres-and-sudo-u-postgres)

[godaddy about sudo - su](https://www.godaddy.com/garage/how-to-install-postgresql-on-ubuntu-14-04/)

[configure pgadmin4 in Server mode](https://www.digitalocean.com/community/tutorials/how-to-install-configure-pgadmin4-server-mode)




