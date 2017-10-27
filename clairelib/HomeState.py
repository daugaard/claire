# A state representation at the home at a specific time.
# This class is based on the CouchDB document class to allow for it to be easily stored and retrieved.

from couchdb.mapping import Document, TextField, IntegerField, BooleanField, DateTimeField, ListField, DictField

class HomeState(Document):
    home_id = TextField()
    type = TextField(default="home_state")
    name = TextField()
    time = DateTimeField()
    periodic_update = BooleanField()
    devices = ListField(DictField())

    def feature_vector(self):
        feature_vector = []
        # Loop over all devices sorted by ID - this will ensure the same order of features for every feature vector
        for device in sorted(self.devices, key=lambda d: d['device_id']):
            device_feature_vector = self.feature_vector_device(device)
            if device_feature_vector != None:
                feature_vector.extend(device_feature_vector)
        return feature_vector

    def output_vector(self):
        output_vector = []
        # Loop over all devices sorted by ID - this will ensure the same order of features for every output vector
        for device in sorted(self.devices, key=lambda d: d['device_id']):
            device_output_vector = self.output_vector_device(device)
            if device_output_vector != None:
                output_vector.extend(device_output_vector)
        return output_vector

    def output_vector_device(self, device):
        if device['type'] == 'DimmerDevice':
            return [device['state']]
        elif device['type'] == 'BinaryPowerSwitchDevice':
            return [1 if device['state'] > 1 else 0]
        else: # Other devices does not generate a feature vector
            return None

    def feature_vector_device(self, device):
        if device['type'] == 'BinarySensorDevice' or device['type'] == 'MultiSensorDevice':
            return [1 if device['state'] > 1 else 0]
        elif device['type'] == 'BinaryPowerSwitchDevice':
            return [device['power_state']]
        else: # Other devices does not generate a feature vector
            return None
