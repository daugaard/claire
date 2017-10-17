from .BasicDevice import BasicDevice

class BinarySensorDevice(BasicDevice):
    def __init__(self, device_id, name, state):
        super(BinarySensorDevice, self).__init__(device_id, name, state)
