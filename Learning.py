import configparser
import logging
import couchdb

from clairelib.HomeState import HomeState
from clairelib.NetworkService import NetworkService
import clairelib.couch.ViewDefinitions as ViewDefinitions

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

# Generate dataset from home states
X = []
y = []
for home in home_states:
    print(home.time)
    X.append(home.feature_vector())
    y.append(home.output_vector())

# Fit to model
print(X,y)

# Store the model
