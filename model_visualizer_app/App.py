from bottle import route, run, template, static_file, request

import sys
import configparser

from datetime import datetime

from clairelib.Home import Home
from clairelib.NetworkService import NetworkService

from sklearn.externals import joblib

demo = True if "demo" in str(sys.argv) else False

config = configparser.ConfigParser()
config.read('config.cfg')

if not "General" in config.sections():
    print("Missing general section in configuration file. Please check config.cfg exists.")
    exit()

# Configuration
home_name = config.get("General", "home_name")

switch_threshold = float(config.get("Automation", "switch_threshold"))
dimmer_threshold = int(config.get("Automation", "dimmer_threshold"))

zware_address = config.get("ZWare", "zware_address")
zware_user = config.get("ZWare", "zware_user")
zware_password = config.get("ZWare", "zware_password")

if demo:
    # Initialize home in debug mode if we start with the demo flag
    print("Starting in DEMO mode.")

    from clairelib.DemoHome import DemoHome

    # Initialize Home model
    home = DemoHome(home_name)

else:
    # Initialize network layer
    network_service = NetworkService(zware_address, zware_user, zware_password)

    # Initialize Home model
    home = Home(home_name, network_service)
    home.update_devices()

# Load prediction models and preprocessing encoder
encoder = joblib.load('./models/feature_vector_encoder.pkl')

output_devices = home.get_home_state().output_devices()
models = {}
for device in output_devices:
    models[device['device_id']] = joblib.load('./models/random_forest_model_device_{}.pkl'.format(device['device_id']))

@route('/')
def index():
    prediction = {}
    device_updated = {}
    for device in output_devices:
        prediction[device['device_id']] = device['state']
        device_updated[device['device_id']] = False

    return template('./model_visualizer_app/views/index', home=home, prediction=prediction, time=datetime.now(), device_updated=device_updated)


@route('/calculate')
def calculate():
    # Extract the new state of the device and update the home state
    for device in home.devices:
        if device.type == 'BinarySensorDevice':
            device.state = int(request.query["{}-state".format(device.device_id)])
            #print('Updated state to {} for BinarySensorDevice device id {}'.format(device.state,device.device_id))
        elif device.type == 'MultiSensorDevice':
            device.state = int(request.query["{}-state".format(device.device_id)])
            device.lux = int(request.query["{}-lux".format(device.device_id)])
            device.temperature = float(request.query["{}-temperature".format(device.device_id)])
            #print('Updated state to {}, {}, {} for MultiSensorDevice device id {}'.format(device.state, device.lux, device.temperature,device.device_id))
        elif device.type == 'BinaryPowerSwitchDevice':
            device.power_state = float(request.query["{}-power_state".format(device.device_id)])
            #print('Updated power state to {} for BinaryPowerSwitchDevice device id {}'.format(device.power_state,device.device_id))

    # Get new home state after updating devices
    home_state = home.get_home_state()

    # Update time stamp
    #timestamp = datetime.strptime(request.query['time'], "%Y-%m-%dT%H:%M")
    home_state.time = datetime.strptime(request.query['time'], "%Y-%m-%dT%H:%M") #timestamp.utcfromtimestamp(timestamp.timestamp())

    # Run through each model
    prediction = {}
    device_updated = {}
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

        # Set device as updated if prediction is different from current state
        if prediction[device['device_id']] != int(request.query["{}-state".format(device['device_id'])]):
            device_updated[device['device_id']] = True
        else:
            device_updated[device['device_id']] = False


    return template('./model_visualizer_app/views/index', home=home, prediction=prediction, time=home_state.time, device_updated=device_updated)


@route('/static/<path:path>')
def callback(path):
    return static_file(path, root="./model_visualizer_app/static/")

run(host='localhost', port=8080, debug=True)
