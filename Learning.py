import configparser
import logging
from time import gmtime

import couchdb

from clairelib.HomeState import HomeState
from clairelib.NetworkService import NetworkService
import clairelib.couch.ViewDefinitions as ViewDefinitions

from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier as ClassificationModel

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

# Generate dataset from home states
X = []
y = []
for home in home_states:
    X.append(home.feature_vector())
    y.append(home.output_vector())

# Now code the time values (weekday, hour and minute) as categorial features in one-of-k (aka one-hot) scheme
encoder = OneHotEncoder(categorical_features=[0,1,2], sparse=False) # One code feature 0,1 and 2
X = encoder.fit_transform(X)

# Split into random training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=gmtime().tm_sec) #2)

# Fit to model
model = ClassificationModel()

model.fit(X_train, y_train)

y_predictions = model.predict(X_test)

# Extract predictions for each output variable and calculate accuracy and f1 score
for ov in range(len(y_test[0])):
    variable_y_predictions = [prediction[ov] for prediction in y_predictions]
    variable_y_test = [test[ov] for test in y_test]
    print("Accuracy Score for output variable {}: {} %".format(ov, round(accuracy_score(variable_y_test, variable_y_predictions, True)*100, 2)))
    #print("F1 Score for output variable {}: {}".format(ov, f1_score(variable_y_test, variable_y_predictions)))

# Store the preprocessor and model

joblib.dump(encoder, "models/feature_vector_encoder.pkl")
joblib.dump(model, "models/random_forest_model.pkl")
