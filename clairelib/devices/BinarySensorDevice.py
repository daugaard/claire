from .BasicDevice import BasicDevice

class BinarySensorDevice(BasicDevice):
    def __init__(self, device_id, name, location, state):
        super(BinarySensorDevice, self).__init__(device_id, name, location, state)
        self.type = "BinarySensorDevice"
