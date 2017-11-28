from .BasicDevice import BasicDevice

class BinaryPowerSwitchDevice(BasicDevice):
    def __init__(self, device_id, name, location, state):
        super(BinaryPowerSwitchDevice, self).__init__(device_id, name, location, state)
        self.type = "BinaryPowerSwitchDevice"
        self.power_state = 0.0

    def to_dict(self):
        d = super().to_dict()
        d['power_state'] = self.power_state
        return d
