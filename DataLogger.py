import datetime
import time
import configparser
import logging
import couchdb

from clairelib.Home import Home
from clairelib.NetworkService import NetworkService

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

logfile = config.get("Log","logfile")
ouput_log_to_console = config.getboolean("Log","ouput_log_to_console")

# Initialize Python logger
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%y %H:%M:%S',
                    filename=logfile,
                    filemode='a')

logger = logging.getLogger('CLAIRE.DataLogger')

if ouput_log_to_console:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

logger.info("Initializing CLAIRE DataLogger Module")

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
    logger.debug("Polling all devices")
    anything_changed = False

    # Has anything changed?
    anything_changed = home.update_devices()

    if anything_changed == True:
        # Store in CouchDB
        logger.info("Something changed - store in CouchDB")
        home_state = home.get_home_state()
        home_state.periodic_update = False
        home_state.store(couchdb)

    else:
        # If more than
        delta = datetime.datetime.now() - last_save

        if (delta.seconds  / 60) >= minutes_between_log:
            # Store in CouchDB
            logger.info("Peridic store in CouchDB")
            home_state = home.get_home_state()
            home_state.periodic_update = True
            home_state.store(couchdb)

            last_save = datetime.datetime.now()

    # Sleep seconds_between_poll
    time.sleep(seconds_between_poll)
