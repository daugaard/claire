import datetime

from .NetworkService import NetworkService

# Home object holds home name and id as well as all the devices in the home.
class Home:
    def __init__(self, name, home_id=""):
        self.network_service = NetworkService()
        self.home_id = home_id
        self.name = name
        self.devices = self.network_service.initialize_devices()

    # Updates the state of each
    def update_devices(self):
        anything_changed = False
        # Poll all devices
        for device in self.devices:
            anything_changed = anything_changed | self.network_service.update_device_state(device)

        return anything_changed

    def to_dict(self):
        h = {'home_id': self.home_id, 'name': self.name, 'devices': []}
        for d in self.devices:
            h['devices'].append( d.to_dict() )

        h['time'] = datetime.datetime.now()

        return h
