from bottle import route, run, template, static_file, request

import configparser

from datetime import datetime

from clairelib.Home import Home
from clairelib.NetworkService import NetworkService

from sklearn.externals import joblib

config = configparser.ConfigParser()
config.read('config.cfg')

if not "General" in config.sections():
    print("Missing general section in configuration file. Please check config.cfg exists.")
    exit()

# Configuration
home_name = config.get("General", "home_name")

zware_address = config.get("ZWare", "zware_address")
zware_user = config.get("ZWare", "zware_user")
zware_password = config.get("ZWare", "zware_password")

# Initialize network layer
network_service = NetworkService(zware_address, zware_user, zware_password)

# Initialize Home model
home = Home(home_name, network_service)
home.update_devices()

# Load prediction models and preprocessing encoder
encoder = joblib.load('./models/feature_vector_encoder.pkl')
model = joblib.load('./models/random_forest_model.pkl')


@route('/')
def index():
    prediction = ""
    return template('./model_visualizer_app/views/index', home=home, prediction=prediction)


@route('/calculate')
def calculate():
    # Extract the new state of the device and update the home state
    for device in home.devices:
        if device.type == 'BinarySensorDevice':
            device.state = int(request.query["{}-state".format(device.device_id)])
            print('Updated state to {} for BinarySensorDevice device id {}'.format(device.state,device.device_id))
        elif device.type == 'MultiSensorDevice':
            device.state = int(request.query["{}-state".format(device.device_id)])
            device.lux = int(request.query["{}-lux".format(device.device_id)])
            device.temperature = float(request.query["{}-temperature".format(device.device_id)])
            print('Updated state to {}, {}, {} for MultiSensorDevice device id {}'.format(device.state, device.lux, device.temperature,device.device_id))
        elif device.type == 'BinaryPowerSwitchDevice':
            device.power_state = float(request.query["{}-power_state".format(device.device_id)])
            print('Updated power state to {} for BinaryPowerSwitchDevice device id {}'.format(device.power_state,device.device_id))

    # Get new home state after updating devices
    home_state = home.get_home_state()

    # Update time stamp
    home_state.time = datetime.strptime(request.query['time'], "%Y-%m-%dT%H:%M")

    # Run through model
    feature_vector = home_state.feature_vector()
    feature_vector = encoder.transform([feature_vector])

    prediction = model.predict(feature_vector)

    return template('./model_visualizer_app/views/index', home=home, prediction=prediction)


@route('/static/<path:path>')
def callback(path):
    return static_file(path, root="./model_visualizer_app/static/")

run(host='localhost', port=8080, debug=True)
