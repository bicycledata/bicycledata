# Deploying Flask app with uwsgi and nginx

## Step 1 — Installing nginx

```bash
sudo apt update
sudo apt install nginx
```

## Step 2 — Checking the web server

```bash
sudo systemctl status nginx
```

```bash
● nginx.service - A high performance web server and a reverse proxy server
    Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: enabled)
    Active: active (running) since Wed 2025-01-22 14:37:31 UTC; 1h 52min ago
    Docs: man:nginx(8)
    Process: 52146 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 52148 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
Main PID: 52149 (nginx)
    Tasks: 3 (limit: 4613)
    Memory: 4.4M (peak: 5.8M)
        CPU: 671ms
    CGroup: /system.slice/nginx.service
            ├─52149 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
            ├─52150 "nginx: worker process"
            └─52151 "nginx: worker process"

Jan 22 14:37:31 bicycledata systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
Jan 22 14:37:31 bicycledata systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
```

## Step 3 — Managing the nginx process

To stop the web server, type:

```bash
sudo systemctl stop nginx
```

To start the web server, type:

```bash
sudo systemctl start nginx
```

To stop and then start the service again, type:

```bash
sudo systemctl restart nginx
```

If you are simply making configuration changes, nginx can often reload
without dropping connections. To do this, type:

```bash
sudo systemctl reload nginx
```

By default, nginx is configured to start automatically when the server
boots. If this is not what you want, you can disable this behavior by
typing:

```bash
sudo systemctl disable nginx
```

To re-enable the service to start up at boot, you can type:

```bash
sudo systemctl enable nginx
```

## Step 4 — Installing the Components from the Ubuntu Repositories

```bash
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

## Step 5 — Creating a Python Virtual Environment

```bash
sudo apt update
sudo apt install python3 python3-venv
```

Create a virtual environment to store your Flask project’s Python
requirements by typing:

```bash
sudo mkdir -p /var/www/bicycledata.vti.se/
cd /var/www/bicycledata.vti.se/
sudo chown fsk:www-data .
python3 -m venv .env/
.env/bin/pip install --upgrade pip
```

This will install a local copy of Python and pip into a directory
called .env within your project directory.

Before installing applications within the virtual environment, you
need to activate it. Do so by typing:

```bash
source .env/bin/activate
```

# Step 6 — Setting Up a Flask Application

Now that you are in your virtual environment, you can install Flask
and uWSGI and get started on designing your application.

First, let's install wheel with the local instance of pip to ensure
that our packages will install even if they are missing wheel
archives:

```bash
pip3 install wheel
```

Next, let's install Flask and uWSGI:

```bash
pip3 install uwsgi flask
```

### Creating a Sample App

Now that you have Flask available, you can create a simple
application. Flask is a microframework. It does not include many of
the tools that more full-featured frameworks might, and exists mainly
as a module that you can import into your projects to assist you in
initializing a web application.

While your application might be more complex, we’ll create our Flask
app in a single file, called `bicycledata.py`:

    > nano ~/bicycledata/bicycledata.py

The application code will live in this file. It will import Flask and
instantiate a Flask object. You can use this to define the functions
that should be run when a specific route is requested:

    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "<h1 style='color:blue'>Hello There!</h1>"

    if __name__ == "__main__":
        app.run(host='127.0.0.1', port=5000)

This basically defines what content to present when the root domain is
accessed. Save and close the file when you're finished.

Now, you can test your Flask app by typing:

    > python3 bicycledata.py

You will see output like the following, including a helpful warning
reminding you not to use this server setup in production:

    Output
    * Serving Flask app bicycledata (lazy loading)
     * Environment: production
     WARNING: Do not use the development server in a production environment.
     Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

When you are finished, hit CTRL-C in your terminal window to stop the
Flask development server.

### Creating the WSGI Entry Point

Next, let's create a file that will serve as the entry point for our
application. This will tell our uWSGI server how to interact with it.

Let’s call the file `wsgi.py`:

    > nano ~/bicycledata/wsgi.py

In this file, let's import the Flask instance from our application and
run it:

    from bicycledata import app

    if __name__ == "__main__":
      app.run(host='127.0.0.1', port=5000)

Save and close the file when you are finished.

We’re now done with our virtual environment, so we can deactivate it:

    > deactivate

Any Python commands will now use the system’s Python environment
again.

### Creating a uWSGI Configuration File

You have tested that uWSGI is able to serve your application, but
ultimately you will want something more robust for long-term usage.
You can create a uWSGI configuration file with the relevant options
for this.

Let’s place that file in our project directory and call it `wsgi.ini`:

```bash
nano /var/www/bicycledata.vti.se/wsgi.ini
```

Let’s put the content of our configuration file:

```bash
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = /var/www/bicycledata.vti.se/wsgi.sock
chmod-socket = 660
vacuum = true

die-on-term = true

logto = /var/www/bicycledata.vti.se/wsgi.log
```

When you are finished, save and close the file.

## Step 7 — Creating a systemd Unit File

Next, let's create a systemd service unit file. Creating a systemd
unit file will allow Ubuntu’s init system to automatically start uWSGI
and serve the Flask application whenever the server boots.

Create a unit file ending in `.service` within the `/etc/systemd/`
system directory to begin:

```bash
sudo nano /etc/systemd/system/bicycledata.vti.se.service
```

Let’s put the content of our server file:

```bash
[Unit]
Description=uWSGI instance to serve bicycledata.vti.se
After=network.target

[Service]
User=fsk
Group=www-data
WorkingDirectory=/var/www/bicycledata.vti.se
Environment="PATH=/var/www/bicycledata.vti.se/.env/bin"
ExecStart=/var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini

[Install]
WantedBy=multi-user.target
```

With that, our systemd service file is complete. Save and close it
now.

We can now start the uWSGI service we created and enable it so that it
starts at boot:

```bash
sudo systemctl start bicycledata.vti.se
sudo systemctl enable bicycledata.vti.se
```

Let’s check the status:

```bash
sudo systemctl status bicycledata.vti.se
```

You should see output like this:

```bash
● bicycledata.vti.se.service - uWSGI instance to serve bicycledata.vti.se
    Loaded: loaded (/etc/systemd/system/bicycledata.vti.se.service; enabled; preset: enabled)
    Active: active (running) since Wed 2025-01-22 14:53:53 UTC; 1h 34min ago
Main PID: 52327 (uwsgi)
    Tasks: 6 (limit: 4613)
    Memory: 155.2M (peak: 155.7M)
        CPU: 2.023s
    CGroup: /system.slice/bicycledata.vti.se.service
            ├─52327 /var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini
            ├─52330 /var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini
            ├─52331 /var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini
            ├─52332 /var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini
            ├─52333 /var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini
            └─52334 /var/www/bicycledata.vti.se/.env/bin/uwsgi --ini wsgi.ini

Jan 22 14:53:53 bicycledata systemd[1]: Started bicycledata.vti.se.service - uWSGI instance to serve bicycledata.vti.se.
Jan 22 14:53:53 bicycledata uwsgi[52327]: [uWSGI] getting INI configuration from wsgi.ini
```

If you see any errors, be sure to resolve them before continuing with
the tutorial.

## Step 8 — Configuring Nginx to Proxy Requests

Our uWSGI application server should now be up and running, waiting for
requests on the socket file in the project directory. Let’s configure
Nginx to pass web requests to that socket using the `uwsgi` protocol.

Begin by creating a new server block configuration file in Nginx’s
`sites-available` directory. Let’s call this `bicycledata` to keep in line
with the rest of the guide:

```bash
sudo nano /etc/nginx/sites-available/bicycledata.vti.se
```

Open up a server block and tell Nginx to listen on the port `80`.
Let’s also tell it to use this block for requests for our server's
domain name:

```bash
server {
    server_name bicycledata.vti.se;
    listen 443 ssl;

    ssl_certificate     /etc/nginx/ssl/star_vti_se.crt;
    ssl_certificate_key /etc/nginx/ssl/star_vti_se.key;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///var/www/bicycledata.vti.se/wsgi.sock;
    }
}

server {
    server_name bicycledata.vti.se;
    listen 80;

    return 301 https://$host$request_uri;
}
```

Save and close the file when you're finished.

To enable the Nginx server block configuration you’ve just created,
link the file to the `sites-enabled` directory:

    > sudo ln -s /etc/nginx/sites-available/bicycledata.vti.se /etc/nginx/sites-enabled

With the file in that directory, we can test for syntax errors by
typing:

    > sudo nginx -t

If this returns without indicating any issues, restart the Nginx
process to read the new configuration:

    > sudo systemctl restart nginx

You should now be able to navigate to your server’s domain name in
your web browser: http://127.0.0.1/

## Step 9 — Managing the application process

Now that you have your application up and running, let's review some
basic management commands.

To stop your application, type:

    > sudo systemctl stop bicycledata

To start the application when it is stopped, type:

    > sudo systemctl start bicycledata

To stop and then start the service again, type:

    > sudo systemctl restart bicycledata

To check the status of the application:

    > sudo systemctl status bicycledata

### Logs

#### Application Logs

`bicycledata/wsgi.log`: Every application request is recorded is in
this log file.

#### Server Logs

`/var/log/nginx/access.log`: Every request to your web server is
recorded in this log file unless Nginx is configured to do otherwise.

`/var/log/nginx/error.log`: Any Nginx errors will be recorded in this
log.

---

Credits:
https://medium.com/swlh/deploy-flask-applications-with-uwsgi-and-nginx-on-ubuntu-18-04-2a47f378c3d2

---
