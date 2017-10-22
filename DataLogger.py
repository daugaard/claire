import datetime
import time
import configparser
import couchdb
from uuid import uuid4

from lib.Home import Home
from lib.NetworkService import NetworkService

config = configparser.ConfigParser()
config.read('config.cfg')

if not "General" in config.sections():
    print("Missing general section in configuration file. Please check config.cfg exists.")
    exit()

# Configuration
minutes_between_log = config.getfloat("DataLogger", "minutes_between_log")
seconds_between_poll = config.getfloat("DataLogger", "seconds_between_poll")

home_name = config.get("General", "home_name")

zware_address = config.get("ZWare", "zware_address")
zware_user = config.get("ZWare", "zware_user")
zware_password = config.get("ZWare", "zware_password")

couchdb_server = config.get("CouchDB", "url")
couchdb_name = config.get("CouchDB", "db")

# Initialize network layer
network_service = NetworkService(zware_address, zware_user, zware_password)

# Initialize Home model
home = Home(home_name, network_service)

# Connect to CouchDB
couch = couchdb.Server(couchdb_server)

try:
    couchdb = couch[couchdb_name]
except couchdb.http.ResourceNotFound:
    couchdb = couch.create(couchdb_name)


# Loop forever
last_save = datetime.datetime(1999,1,1)

while True:
    print("Polling all devices")
    anything_changed = False

    # Has anything changed?
    anything_changed = home.update_devices()

    if anything_changed == True:
        # Store in CouchDB
        print("Something changed - store in CouchDB")
        home_state = home.get_home_state()
        home_state.store(couchdb)

    else:
        # If more than
        delta = datetime.datetime.now() - last_save

        if (delta.seconds  / 60) >= minutes_between_log:
            # Store in CouchDB
            print("Peridic store in CouchDB")
            home_state = home.get_home_state()
            home_state.store(couchdb)

            last_save = datetime.datetime.now()

    # Sleep seconds_between_poll
    time.sleep(seconds_between_poll)
