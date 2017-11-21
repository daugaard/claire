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
        # Append with day of week
        feature_vector.append( self.time.weekday() )

        # Append with hour and minute number in 10 minutes interval
        feature_vector.append( self.time.hour )
        feature_vector.append( int(self.time.minute/10) )

        # Loop over all devices sorted by ID - this will ensure the same order of features for every feature vector
        for device in sorted(self.devices, key=lambda d: d['device_id']):
            device_feature_vector = self.feature_vector_device(device)
            if device_feature_vector != None:
                feature_vector.extend(device_feature_vector)

        return feature_vector

    def feature_vector_for_output_device(self, output_device):
        feature_vector = []
        # Append with day of week
        feature_vector.append( self.time.weekday() )

        # Append with hour and minute number in 10 minutes interval
        feature_vector.append( self.time.hour )
        feature_vector.append( int(self.time.minute/10) )

        # Loop over all devices sorted by ID - this will ensure the same order of features for every feature vector
        for device in sorted(self.devices, key=lambda d: d['device_id']):
            if output_device['device_id'] != device['device_id']:
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

    def output_devices(self):
        return [device for device in self.devices if device['type'] in ('BinaryPowerSwitchDevice','DimmerDevice')]

    def output_vector_device(self, device):
        if device['type'] == 'DimmerDevice':
            return [device['state']]
        elif device['type'] == 'BinaryPowerSwitchDevice':
            return [1 if device['state'] > 1 else 0]
        else: # Other devices does not generate a feature vector
            return None

    def output_vector_for_device_id(self, device_id):
        # Find output device based on id
        device = next(device for device in self.devices if device['device_id'] == device_id)
        if device['type'] == 'DimmerDevice':
            return device['state']
        elif device['type'] == 'BinaryPowerSwitchDevice':
            return 1 if device['state'] > 1 else 0
        else: # Other devices does not generate a feature vector
            return None

    def feature_vector_device(self, device):
        if device['type'] == 'BinarySensorDevice':
            return [1 if device['state'] > 1 else 0]
        elif device['type'] == 'MultiSensorDevice':
            return [1 if device['state'] > 1 else 0, device['lux']]
        elif device['type'] == 'BinaryPowerSwitchDevice':
            return [device['power_state']]
        else: # Other devices does not generate a feature vector
            return None
