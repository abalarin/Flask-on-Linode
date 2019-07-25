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

#### If you retrieve your app from source control:
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

#### If you're copying it directly from your Local Machine
1. SCP your Applications root directory into your Linode's Home directory
```
scp -r your_app/ root@<Linode-IP>:/home
```


## Configure Environment Variables
If your application has environment variables you may want to move them into a configuration file. This can be skipped if you Project doesnt have any environment vairables.
1. Create a configuration file for any of the environment variable for your Application.
```
nano /etc/config.json
{
	"SECRET_KEY": "1A37BbcCJh67",
	"SQLALCHEMY_DATABASE_URI": "sqlite:///site.db"
}
```

2. Modify your Flask config to import the newly created configuration.
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
2. Create NGINX Configuration File. Since we are using Gunicorn you can copy off of their [NGINX configuration](https://gunicorn.org/#deployment) to start.
```
# If you dont have a domain you will want to insert your Linodes IP
sudo nano /etc/nginx/sites-enabled/flaskapp
```

3. Unlink the NGINX default config
```
unlink /etc/nginx/sites-enabled/default
```
4. Reload your NGINX Server
```
sudo nginx -s reload
```

## Install Python and Packages
You should now be in your application root directory on your Linode.
1. Install Python 3
```
sudo apt install python3
```
2. Install pip
```
sudo apt install python3-pip
```
3. Install Flask Packages/libraries
```
pip3 install -r requirements.txt
```

## Deploy your Application
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.

1. Install Gunicorn
```
pip3 install gunicorn
```
2. You are going to want to run Gunicorn from your applications root directory
```
gunicorn -w 3 flask_app:app
```

#### Your Application is now live!! You should be able to navigate to it by entering your Linodes IP into a browser.

## Configure Supervisor
Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems. Supervisor is great for auto-reloading gunicorn if it crashes or your Linode needs to be rebooted.
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
- Adding a FQDN
- Containerizing Your App
