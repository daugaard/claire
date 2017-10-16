# Hold a simple device and its state
class BasicDevice:

    def __init__(self, device_id, name, state):
        self.device_id = device_id
        self.name = name
        self.state = state


    def to_dict(self):
        d = {'device_id': self.device_id, 'name': self.name, 'state': self.state}
        return d
