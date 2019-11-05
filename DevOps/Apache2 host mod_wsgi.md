

## Apache2 Background


### Apache2 virutal host 


* site-available 

all virtual hosts are configured in individual files with `/etc/apache2/sites-available` 


* site-enabled 

until the *.config in site-available are enabled, Apache2 won't know know.

	sudo sevice apache2 reload 

* IP based virtual host 

use IP address of the connection to determine the correct virtual host to serve, so each host needs a separate IP


we had name-based vhost in LAN, a few web servers sharing the same IP in the same physical machine, but with different Ports, and even we don't use DNS server to tell the domains. 


### apache mode cores 

[refer](https://httpd.apache.org/docs/2.4/mod/core.html#servername)


* VirtualHost 

the title to define this virutal host, and tell which port to listen. by default is port80


* ServerName

sets the request scheme, hostname, and port that the server uses to identify itself

* ServerAlias

sets the alternate name for a host 

* WSGIDaemonProcess

for wsgi app, which usually define in a seperate Python virtual environment, rather than the default localhost user or root. so `WSGIDaemonProcess` point to the python virtual env. 

* WSGIScriptAlias

point to the wsgi_app.wsgi 

* DocumentRoot 

set the directory from which httpd/apache2 will serve files `/var/www/html`




## mod_wsgi 

       
* install `apt-get install apache2  libapache2-mode-wsgi-py3`

### config in Apache2 

#### config with configure file 
    
* create  `example.conf` under  `/etc/apache2/conf-available/`

```script 
<VirtualHost *:8084>
        ServerName  10.20.181.119:8084
        ServerAlias example.com
        DocumentRoot "/var/www/html"
        ErrorLog "/var/www/example/logs/error.log"
 
</VirtualHost>
``` 
the served web content is stored at `/var/www/html`, which can simple include a index.html or a few js.

* enable configure, which will create corresponding conf under `conf-enable` folder

        sudo a2enconf example 

* check configure

        sudo apachectl -S 
        sudo apachectl configtest 


#### config with virtual host 

* create `example.conf` under  `/etc/apache2/site-available/`
```script 
<VirtualHost *:8085>
        ServerName  10.20.181.119:8085
        ServerAlias application.com
        DocumentRoot "/var/www/wsgy_example"
        ErrorLog "/var/www/wsgy_example/logs/error.log"
        WSGIScriptAlias /application /var/www/wsgy_app/application.wsgi

</VirtualHost>
```

here used the additional `WSGI script`, [link](https://www.linode.com/docs/web-servers/apache/apache-and-modwsgi-on-ubuntu-14-04-precise-pangolin/)

```script 

import os
import sys

sys.path.append('/var/www/wsgy_app/')

os.environ['PYTHON_EGG_CACHE'] = '/var/www/wsgy_app/.python-egg'

def application(environ, start_response):
        status = '200 OK'
        output = b'Helo World'

        response_headers = [('Content-type', 'text/plain'),
                            ('Content-length', str(len(output)))]

        start_response(status, response_headers)

        return [output]
```

* enable configure, which will create corresponding conf under `site-enable` folder

        sudo a2ensite wsgy_example 

* check configure

        sudo apachectl -S 
        sudo apachectl configtest 


### add multi ports:

in /etc/apache2/ports.conf:

    Listen 8083
    Listen 8084

since this Apache server host system_engineering web and pgadmin4 web, and share the same IP.

### restart apache 
 
      sudo systemctl restart apache2 


### test apache

in browser:

     10.20.181.119:8085/application

should view "hello world"



## refer

[name based virtual host](https://httpd.apache.org/docs/2.4/vhosts/name-based.html)

[Apache2 virutal host](https://httpd.apache.org/docs/2.4/vhosts/)

[vhost with different ports](https://serverfault.com/questions/246445/how-do-i-create-virtual-hosts-for-different-ports-on-apache)




