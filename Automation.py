import datetime
import time
import configparser
import logging
import couchdb

from clairelib.Home import Home
from clairelib.NetworkService import NetworkService

from sklearn.externals import joblib

config = configparser.ConfigParser()
config.read('config.cfg')

if not "General" in config.sections():
    print("Missing general section in configuration file. Please check config.cfg exists.")
    exit()

# Configuration
seconds_between_poll = config.getfloat("Automation", "seconds_between_poll")
minutes_between_log = config.getfloat("Automation", "minutes_between_log")

switch_threshold = float(config.get("Automation", "switch_threshold"))
dimmer_threshold = int(config.get("Automation", "dimmer_threshold"))

home_name = config.get("General", "home_name")

zware_address = config.get("ZWare", "zware_address")
zware_user = config.get("ZWare", "zware_user")
zware_password = config.get("ZWare", "zware_password")

couchdb_server = config.get("CouchDB", "url")
couchdb_name = config.get("CouchDB", "db")

logfile = config.get("Log","automation_logfile")
ouput_log_to_console = config.getboolean("Log","ouput_log_to_console")

# Load preprocessing encoder
encoder = joblib.load('./models/feature_vector_encoder.pkl')

# Initialize Python logger
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%y %H:%M:%S',
                    filename=logfile,
                    filemode='a')

logger = logging.getLogger('CLAIRE.Automation')

if ouput_log_to_console:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

logger.info("Initializing CLAIRE Automation Module")

# Initialize network layer
network_service = NetworkService(zware_address, zware_user, zware_password)

# Initialize Home model
home = Home(home_name, network_service)

# Load all prediction models
output_devices = home.get_home_state().output_devices()
models = {}
for device in output_devices:
    models[device['device_id']] = joblib.load('./models/random_forest_model_device_{}.pkl'.format(device['device_id']))

# Connect to CouchDB
couch = couchdb.Server(couchdb_server)

try:
    couchdb = couch[couchdb_name]
except couchdb.http.ResourceNotFound:
    couchdb = couch.create(couchdb_name)

# Loop forever
last_save = datetime.datetime(1999,1,1)

while True:
    logger.info("Polling all devices")
    anything_changed = False

    # Update devices
    anything_changed = home.update_devices()

    if anything_changed:
        # Store in CouchDB
        logger.info("Something changed - store in CouchDB")

        # Sample the current state
        home_state = home.get_home_state()
        home_state.periodic_update = False
        home_state.store(couchdb)

        # Predict
        predictions = {}
        for device in output_devices:
            feature_vector = home_state.feature_vector_for_output_device(device)
            feature_vector = encoder.transform([feature_vector])

            # Preform prediction
            if device['type'] == 'BinaryPowerSwitchDevice':
                # Return probablity of switch being on
                probabilities = prediction[device['device_id']] = models[device['device_id']].predict_proba(feature_vector)[0]
                # Prediction thredshold set at 40% if algorithm is 40% sure the binary switch is no - turn it on
                prediction[device['device_id']] = 255 if prediction[device['device_id']][1] > switch_threshold else 0
            else:
                prediction[device['device_id']] = models[device['device_id']].predict(feature_vector)
                prediction[device['device_id']] = int(prediction[device['device_id']]) if prediction[device['device_id']] > dimmer_threshold else 0

        # Does prediction match current state
        for device in home_state.output_devices():
            # If prediction is different from output vector we need to update the state
            if predictions[device['device_id']] != home_state.output_vector_device(device):
                # Execute automation to make state match the predicted state from the machine learning model
                logger.info(str.format("Device {} state {} differs from prediction {}. Executing automation.",device['name'], device['state'], predictions[device['device_id']]))
                # Actually change the state
                home.change_device_state(device['device_id'], predictions[device['device_id']][0])
    else:
        # If more than X since last save also store in couchdb
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
