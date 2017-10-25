# Hold a simple device and its state
class BasicDevice:

    def __init__(self, device_id, name, state):
        self.device_id = device_id
        self.name = name
        self.state = state
        self.type = "BasicDevice"

    def to_dict(self):
        d = {'device_id': self.device_id, 'name': self.name, 'state': self.state, 'type': self.type}
        return d
