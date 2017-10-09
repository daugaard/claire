import datetime

# Home object holds home name and id as well as all the devices in the home.
class Home:
    def __init__(self, home_id, name):
        self.home_id = home_id
        self.name = name
        self.devices = []

    def to_dict(self):
        h = {'home_id': self.home_id, 'name': self.name, 'devices': []}
        for d in self.devices:
            h['devices'].append( d.to_dict() )

        h['time'] = datetime.datetime.now()

        return h

# Hold a simple device and its state
class BasicDevice:

    def __init__(self, device_id, state, name):
        self.device_id = device_id
        self.name = name
        self.state = state


    def to_dict(self):
        d = {'device_id': self.device_id, 'name': self.name, 'state': self.state}
        return d
