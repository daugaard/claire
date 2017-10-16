import datetime

from .NetworkService import NetworkService

# Home object holds home name and id as well as all the devices in the home.
class Home:
    def __init__(self, name, home_id=""):
        self.network_service = NetworkService()
        self.home_id = home_id
        self.name = name
        self.devices = self.network_service.initialize_devices()

    def to_dict(self):
        h = {'home_id': self.home_id, 'name': self.name, 'devices': []}
        for d in self.devices:
            h['devices'].append( d.to_dict() )

        h['time'] = datetime.datetime.now()

        return h
