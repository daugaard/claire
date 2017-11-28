from .BasicDevice import BasicDevice

class MultiSensorDevice(BasicDevice):
    def __init__(self, device_id, name,location, state):
        super(MultiSensorDevice, self).__init__(device_id, name, location, state)
        self.type = "MultiSensorDevice"
        self.temperature = 0.0
        self.lux = 0

    def to_dict(self):
        d = super().to_dict()
        d['temperature'] = self.temperature
        d['lux'] = self.lux

        return d
