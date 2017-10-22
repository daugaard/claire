# Installing and running the data logger application on a fresh Raspberry Pi

Download and install Raspberry Pi image as detailed here: http://zwavepublic.com/developer, plug in the Z-Wave bridge adapter and boot the Raspberry Pi.

Next access the Z-Ware sample gateway software using https://raspberrypi.local/ui/pc/index.html and setup your network by installing your devices.

## Installing prerequisites
SSH to your Raspberry Pi and install Python3, pip3, couchdb, screen and git.
```
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install couchdb
sudo apt-get install screen git
```
Now install the CouchDB Python module.
```
sudo pip3 install couchdb
```
### Enabling external access to CouchDB
Enable external access to CouchDB by allowing it to bind to your local IP.
```
cd /etc/couchdb
sudo nano default.ini
```
Change the following section:
```ini
[httpd]
port = 5984
bind_address = 127.0.0.1
```
To:
```ini
[httpd]
port = 5984
bind_address = 0.0.0.0
```
And restart couchdb:
```
sudo service restart couchdb
```

Verify couchdb was installed and you can access from your computer by going to: http://raspberrypi.local:5984/_utils, you should see the Apache CouchDB Futon Overview.


## Cloning the repository and run the code
At this point we're ready to clone the CLAIRE respository and start the data logger.

```
git clone https://github.com/daugaard/claire.git
```

Create a new config file and configure as appropriate for your installation:
```
cd claire
cp config.cfg.default config.cfg
nano config.cfg
```
If you're ready to start the CLAIRE datalogger do so by starting a screen, executing the datalogger script and exit the screen by pressing Ctrl+a+d to detach.
```
screen
python3 DataLogger.py
(Ctrl+a+d)
```
You can following along in the log file like this:
```
tail log/claire_datalogger.log
```
If you need to start the datalogger, enter the screen, press Ctrl+C to exit and restart.
```
screen -r
(Ctrl+c)
python3 DataLogger.py
(Ctrl+a+d)
```
