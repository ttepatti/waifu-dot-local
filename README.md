# waifu-dot-local

The waifu dot local image delivery service.

| Desktop | Mobile |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
![Screenshot of waifu.local on Desktop](waifu-dot-local_example_screenshot.png) | ![Screenshot of waifu.local on Mobile](waifu-dot-local_example_screenshot_mobile.png)

This is a web service that displays a random image every time the page is reloaded. It's intended to be ran on your local network to serve other LAN devices.

I made this so that I could load it up with anime wallpapers and use it as a background/screensaver/etc. for devices on my local network. With the way the CSS is set up, it tries its best to scale the loaded image to your current device's screen size, filling the screen as much as possible to act as a wallpaper.

It's pretty hacky so it may need custom modifications (such as paths, CSS, etc.) based on your installation/needs/etc. I'm mainly putting it on GitHub so that I don't lose the code.

Enjoy!

## Installation

System Requirements:
- python3
- python3-pip
- python3.12-venv (or whatever your python version is)

Python Requirements:
- flask

To install, first we need a venv:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

Next, install python dependencies:
```sh
pip3 install flask
```

Now, if you just want to run the service you can execute waifu.py. Done!

## Making it Production-Ready(?) with Gunicorn

Now, flask gave me a million warnings about "not running directly from flask for a production app" :unamused: so I decided to shove it behind Gunicorn to make it slightly more legit, especially because I want to use it as a service on my home network long-term.

Make sure you're in the top level directory with the pyproject file and run:
```sh
pip3 install .
```

This will install the package as 'waifudotlocal'

Next, use your proxy/WSGI of choice. I chose gunicorn:
```sh
python3 install gunicorn
```

And then, to run:
```sh
gunicorn -w 4 -b 0.0.0.0 'waifudotlocal:create_app()'
```

Your output should be something like:

```
(.venv) tim@waifu:~/waifu-dot-local$ gunicorn -w 4 -b 0.0.0.0 'waifudotlocal:create_app()'
[2025-11-15 22:38:08 +0000] [3954] [INFO] Starting gunicorn 23.0.0
[2025-11-15 22:38:08 +0000] [3954] [INFO] Listening at: http://0.0.0.0:8000 (3954)
[2025-11-15 22:38:08 +0000] [3954] [INFO] Using worker: sync
[2025-11-15 22:38:08 +0000] [3955] [INFO] Booting worker with pid: 3955
[2025-11-15 22:38:08 +0000] [3956] [INFO] Booting worker with pid: 3956
[2025-11-15 22:38:08 +0000] [3957] [INFO] Booting worker with pid: 3957
[2025-11-15 22:38:08 +0000] [3958] [INFO] Booting worker with pid: 3958
```

Congrats! Navigate to your current hostname + port 8000 to browse.

### Hard Mode: TLS + Gunicorn

I apparently hate having free time, so I was like "damn, I should get Gunicorn up and running with TLS!"

It's not actually *that* bad to get up and running, but if you don't already have a root CA for your home network and some understanding of TLS, it's going to be a pain.

I'm not going to dive too much into it here, but you can run gunicorn + TLS by changing the command to:

```sh
gunicorn --certfile=waifu.crt --keyfile=waifu.key -w 4 -b 0.0.0.0 'waifudotlocal:create_app()'
```

(Where the certificate/key are the specific pair you made for this service, signed by your local network root CA)

## Running as a Service with Supervisor

**You:** I don't want to log into my VM every time this thing goes offline!!
**The humble supervisord:** :kiss:

If you want it to start at boot, you can daemonize it with supervisord!

First, we gotta make our launcher script. Create a file called "waifudotlocal_launcher.sh" and fill it with:

```sh
#!/bin/bash
# Uncomment the commented lines if you're using TLS + Gunicorn
NAME="waifudotlocal"
VENVDIRECTORY="/home/tim/waifu-dot-local/.venv/"
CONNECTIONS=4
IPADDR="0.0.0.0:8000"
#IPADDR="0.0.0.0:8443"
#SSLCERT="/home/tim/waifu.crt"
#SSLKEY="/home/tim/waifu.key"

echo "Launching waifudotlocal service"

cd $VENVDIRECTORY
source bin/activate
gunicorn -w $CONNECTIONS -b $IPADDR 'waifudotlocal:create_app()'
#gunicorn --certfile=$SSLCERT --keyfile=$SSLKEY -w $CONNECTIONS -b $IPADDR 'waifudotlocal:create_app()'
```

All this script does is launch our service when run - easy enough! Feel free to run it now if you want to make sure you got all of the commands and paths right. (Oh, that being said: Swap any of the paths used above with your own!)

Next, we'll install supervisord:
```sh
sudo apt install supervisor
```

then, we have to create a custom configuration for our service:
```sh
sudo vim /etc/supervisor/conf.d/waifu.conf
```

our custom configuration will essentially just execute our launcher script at boot, and log all printed messages to the log file we specify!
```
[program:waifudotlocal]
command = /home/tim/waifu-dot-local/waifudotlocal_launcher.sh
user = tim
stdout_logfile = /home/tim/waifu-dot-local/waifudotlocal_supervisor.log
redirect_stderr = true
```

Now, reread all loaded configurations and update with supervisor:
```sh
$ sudo supervisorctl reread
waifudotlocal: available
$ sudo supervisorctl update
waifudotlocal: added process group
```

And finally, to check the status of our service:
```sh
$ sudo supervisorctl status waifudotlocal
waifudotlocal               RUNNING pid 4750, uptime 0:00:09
```

Woohoo, now it should start at boot. Reboot your server if you want to give it a shot?

## Directories

As some background to the structure of the project:

### templates/

This holds any template pages for the webapp. Because this app has a single page, there is only one.

### static/waifus/

This holds any waifu images. Fill this directory to your heart's content!
