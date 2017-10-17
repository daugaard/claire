from .BasicDevice import BasicDevice

class BinaryPowerSwitchDevice(BasicDevice):
    def __init__(self, device_id, name, state):
        super(BinaryPowerSwitchDevice, self).__init__(device_id, name, state)
