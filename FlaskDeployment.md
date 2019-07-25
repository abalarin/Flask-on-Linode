# Flask-on-Linode
If you are just learning how to use Python and have started dabbling with Web Applications that interact with persistent data, then this guide may help you deploy your app!

The goal is to deploy our web application with as little configuration and server management as possible.

#### Tech Used
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/1.0.x/)
- [NGINX](https://www.nginx.com/resources/wiki/)
- [Gunicorn](http://docs.gunicorn.org/en/stable/)
- Supervisor

## Table of Contents
- [Before You Begin](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#before-you-begin)
- [Move your App to your Linode](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#move-your-app-to-your-linode)
- [Configure Environment Variables](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#configure-environment-variables)
- [Configure NGINX](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#configure-nginx)
- [Install Python and Packages](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#install-python-and-packages)
- [Deploy your Application](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#deploy-your-application)
- [Configure Supervisor](https://github.com/abalarin/Flask-on-Linode/blob/master/FlaskDeployment.md#configure-supervisor)

## Before You Begin
You'll want to make sure you have already built out a Flask Application that you are ready to deploy to a production environment. If you haven't already created an app or its still under constructions you can use this [Simple Flask Blog Application](https://github.com/abalarin/Flask-on-Linode) for this tutorial.

We are also going to assume that you have already run through the [Getting Started with Linode](https://www.linode.com/docs/getting-started/) Guide and can SSH into your Linode.

You may want to source control your project with [git](https://github.com) so that later down the road you can implement Continuous Integration/Deployment development into your application.

## Move your App to your Linode
So you have finished developing your shiny Python Flask Application and want to deploy it to a production environment for the world to see. You can either retrieve your app from source control or SCP it from your Local Machine.

#### Retrieving your Application from source control
1. SSH into your Linode
```
ssh user@<Linode-IP>
```
2. Navigate to your Home directory
```
cd /home
```
3. Pull from source control (Replace my repo with yours)
```
git clone https://github.com/abalarin/Flask-on-Linode.git
```

#### Retrieving your Application from your Local Machine
1. SCP your Applications root directory into your Linode's Home directory
```
scp -r flask_app/ user@<Linode-IP>:/home
```


## Configure Environment Variables
If your application has environment variables you may want to move them into a configuration file. This can be skipped if you Project doesn't have any environment variables.

The following are rudimentary examples of some environment variables that you might have on your application.
1. Create a configuration file for any of the environment variables for your Application.
```
sudo nano /etc/config.json
```
```
{
	"SECRET_KEY": "1A37BbcCJh67",
	"SQLALCHEMY_DATABASE_URI": "sqlite:///site.db"
}
```

2. Modify your Flask configuration and import the newly created json config.
```
import json
import urllib3

  with open('/etc/config.json') as config_file:
    config = json.load(config_file)

  app.config['SECRET_KEY'] = config.get('SECRET_KEY')
  app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
```

## Configure [NGINX](https://www.nginx.com/)
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.
1. Install NGINX
```
sudo apt install nginx
```
2. Create an NGINX Configuration file
```
sudo nano /etc/nginx/sites-enabled/flaskapp
```
```
server {
	listen 80;
	server_name <Your Linodes IP>;

	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
}
```
3. Unlink the NGINX default config
```
unlink /etc/nginx/sites-enabled/default
```
4. Reload your NGINX server
```
sudo nginx -s reload
```

###### If you try navigating to your Linode's IP in a web browser you should get the following or a similar error.
![NGINX Bad Gateway](https://us-east-1.linodeobjects.com/linodestuff/badgateway.png)
###### Next we are going to set up our Web Server Gateway Interface (WSGI) so that NGINX can communicate with our application and the internet can enjoy our stuff.

## Install Python and Packages
You should now be in your applications root directory on your Linode.
1. Install [Python 3](https://www.python.org/download/releases/3.0/)
```
sudo apt install python3
```
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
```
sudo apt install python3-pip
```
3. Install Flask Packages/libraries. If you are using the example [Flask Blog Application](https://github.com/abalarin/Flask-on-Linode) then the packages will be located in requirements.txt
```
pip3 install -r requirements.txt
```

## Deploy your Application
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.

1. Install Gunicorn
```
pip3 install gunicorn
```
2. Run Gunicorn from your Application's root directory or a directory up from your Application's entry point. In the below example we are telling Gunicorn to look for the WSGI instance named _app_ in the _flask_app_ directory. In our [example project](https://github.com/abalarin/Flask-on-Linode) this WSGI instance named _app_ is located in `__init__.py`.
```
gunicorn -w 3 flask_app:app
```
You can also specify the amount of workers you want Gunicorn to use with the `-w` flag. A good rule of thumb is double your CPU core's and add 1. For a Nanode with 1 CPU core thats 3 workers.

#### Your Application is now live!! You should be able to navigate to it by entering your Linodes IP into a web browser.

## Configure Supervisor
Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems. Supervisor is great for auto-reloading gunicorn if it crashes or if your Linode is rebooted unexpectedly.
1. Install Supervisor
```
sudo apt install supervisor
```
2. Create a Supervisor program
```
sudo nano /etc/supervisor/conf.d/flaskapp.conf
```
```
[program:flaskapp]
directory=/home/Flask-on-Linode
command=gunicorn -w 3 flask_app:app
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flaskapp/flaskapp.err.log
stdout_logfile=/var/log/flaskapp/flaskapp.out.log
```
2. create your log files
```
sudo mkdir /var/log/flaskapp
touch /var/log/flaskapp/flaskapp.out.log
touch /var/log/flaskapp/flaskapp.err.log
```

3. Reload Supervisor to apply changes
```
sudo supervisorctl reload
```

# Whats Next
- Deploying a Production Database
- Adding a FQDN
- Containerizing Your Application
