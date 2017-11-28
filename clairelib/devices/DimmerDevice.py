from .BasicDevice import BasicDevice

class DimmerDevice(BasicDevice):
    def __init__(self, device_id, name, location, state):
        super(DimmerDevice, self).__init__(device_id, name, location, state)
        self.type = "DimmerDevice"
