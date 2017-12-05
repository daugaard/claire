import configparser
import logging
from time import gmtime
from datetime import datetime, timedelta

import couchdb

from clairelib.HomeState import HomeState
from clairelib.NetworkService import NetworkService
import clairelib.couch.ViewDefinitions as ViewDefinitions

from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier as ClassificationModel
from sklearn.ensemble import RandomForestClassifier as RegressionModel

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

from sklearn.externals import joblib

config = configparser.ConfigParser()
config.read('config.cfg')

if not "General" in config.sections():
    print("Missing general section in configuration file. Please check config.cfg exists.")
    exit()

# Configuration
home_name = config.get("General", "home_name")

couchdb_server = config.get("CouchDB", "url")
couchdb_name = config.get("CouchDB", "db")

logfile = config.get("Log","logfile")
ouput_log_to_console = config.getboolean("Log","ouput_log_to_console")

# Connect to CouchDB
couch = couchdb.Server(couchdb_server)

try:
    couchdb = couch[couchdb_name]
except couchdb.http.ResourceNotFound:
    print("Error database $(couchdb_name)s does not exist")

# Sync all views
ViewDefinitions.sync(couchdb)

# Load all home states in the database
home_states = HomeState.view(couchdb, "_design/home_state/_view/by_time")

first_home_state = HomeState.view(couchdb, "_design/home_state/_view/by_time", limit=1).rows[0]

# Use this code if you only want to train on a subset of data
#home_states = home_states[str(datetime.now()-timedelta(days=14)):str(datetime.now())]

# Get all output devices in this home
output_devices = first_home_state.output_devices()

# Generate dataset from home states for each output device
Xs = {}
ys = {}
for device in output_devices:
    print("Generating training set for", device['name'])
    # Initialize empty X and y datasets for out output device
    Xs[device['device_id']] = []
    ys[device['device_id']] = []
    # For each home state generate the datasets
    for home in home_states:
        Xs[device['device_id']].append(home.feature_vector_for_output_device( device ))
        ys[device['device_id']].append(home.output_vector_for_device_id( device['device_id'] ))

# Now code the time values (weekday, hour and minute) as categorial features in one-of-k (aka one-hot) scheme
encoder = OneHotEncoder(categorical_features=[0,1,2], sparse=False) # One code feature 0,1 and 2

for device in output_devices:
    print("Training model for", device['name'], "with type", device['type'])
    X = Xs[device['device_id']]
    y = ys[device['device_id']]

    # Encode time values using encoder
    X = encoder.fit_transform(X)

    # Split into random training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=gmtime().tm_sec) #2)

    # Fit to model
    if device['type'] == 'BinaryPowerSwitchDevice':
        model = ClassificationModel()
    else:
        model = RegressionModel()

    model.fit(X_train, y_train)

    y_predictions = model.predict(X_test)

    # Score predictions - calculate accuracy and f1 score
    print("Accuracy Score: {} %".format(round(accuracy_score(y_test, y_predictions, True)*100, 2)))

    # Store the preprocessor and model
    joblib.dump(model, "models/random_forest_model_device_{}.pkl".format(device['device_id']))

# Store encoder
joblib.dump(encoder, "models/feature_vector_encoder.pkl")
