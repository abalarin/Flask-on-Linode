# Flask-on-Linode
If you are just learning how to use Python and have started dabbiling with Web Applications that interact with persistant data, then this guide may help you deploy your app!

The goal is to deploy our web application with as little configuration and server managment as possible.

#### Tech Used
- Python
- Flask
- Nginx
- Gunicorn
- Supervisor

#### Infrastructure
- Ubuntu 19.04
- Nanode, 1GB RAM, 1CPU Linode

## Table of Contents
- Flask-on-Linode
- Table of Contents
- Before You Begin
- Get your App on your Linode
- Installing Python and pip
- Configuring your environment variables
- Configure NGINX
- Install Python and Packages
- Run your Application
- Configure Supervisor

## Before You Begin
You'l want to make sure you have already built out a Flask Application that you are ready to deploy to a production environment. If you haven't already created your app or its still under constructions you can use this [basic blog App](https://github.com/abalarin/Flask-on-Linode)

We are also going to assume that you have already run through the [getting started guide](https://www.linode.com/docs/getting-started/) and can SSH into your Linode.

Lastly, you may want to source control your project with [git](https://github.com).

## Get your App on your Linode
You can either retrieve your app from source control or SCP it from your Local Machine.

#### If you retrieve your app from source control:
1. SSH into your Linode
```
ssh user@<Linode-IP>
```
2. Navigate to your Home directory
```
cd /home
```
3. Pull from source control
```
git clone https://github.com/abalarin/Flask-on-Linode.git
```

#### If you're copying it directly from your Local Machine
1. SCP your Applications root directory onto your Linode Home directory
```
scp -r your_app/ root@<Linode-IP>:/home
```


## Configuring your environment variables
If your application has environment variables you may want to move them into a configuration file.
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

## Configure NGINX
1. Install NGINX
```
sudo apt install nginx
```
2. Create NGINX Configuration File
```
sudo nano /etc/nginx/sites-enabled/flaskapp
```

3. Unlink NGINX default config
```
unlink /etc/nginx/sites-enabled/default
```
4. Reload
```
sudo nginx -s reload
```

## Install Python and Packages
1. Install Python 3
```
sudo apt install python3
```
2. Install pip
```
sudo apt install python3-pip
```
3. Install Flask Packages
```
pip3 install -r requirements.txt
```

## Run your Application
1. Install Gunicorn
```
install gunicorn
```
2. Run it
```
gunicorn -w 3 flask_blog:app
```

## Configure Supervisor
1. Install Supervisor
```
sudo apt install supervisor
```
```
sudo nano /etc/supervisor/conf.d/flaskapp.conf
[program:flaskapp]
directory=/home/flask_blog
command=/home/flask_blog/venv/bin/gunicorn -w 3 flask_blog:app
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
