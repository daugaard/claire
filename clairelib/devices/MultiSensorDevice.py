from .BasicDevice import BasicDevice

class MultiSensorDevice(BasicDevice):
    def __init__(self, device_id, name, state):
        super(MultiSensorDevice, self).__init__(device_id, name, state)
        self.type = "MultiSensorDevice"
        self.temperature = 0.0
        self.lux = 0

    def to_dict(self):
        d = super().to_dict()
        d['temperature'] = self.temperature
        d['lux'] = self.lux

        return d
