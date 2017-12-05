import datetime
from .HomeState import HomeState
from .devices.DimmerDevice import DimmerDevice
from .devices.BinaryPowerSwitchDevice import BinaryPowerSwitchDevice
from .devices.BinarySensorDevice import BinarySensorDevice
from .devices.MultiSensorDevice import MultiSensorDevice

# DemoHome object holds home name and id as well as all the devices in the home.
class DemoHome:
    def __init__(self, name, home_id="ECDEDE49"):
        self.name = name
        self.home_id = home_id
        self.devices = self.initialize_devices()


    def initialize_devices(self):
        devices = []

        devices.append( BinaryPowerSwitchDevice(264, "AVSWITCH", "LIVINGROOM", 0))
        devices.append( DimmerDevice(263, "LIGHT1", "LIVINGROOM", 0) )
        devices.append( DimmerDevice(262, "LIGHT2", "OFFICE", 0) )

        devices.append( BinarySensorDevice(266, "MOTION1", "LIVINGROOM", 0) )
        devices.append( MultiSensorDevice(267, "MOTION2", "OFFICE", 0) )

        return devices

    def get_home_state(self):
        h = HomeState(home_id=self.home_id, name=self.name, time=datetime.datetime.now())
        for d in self.devices:
            h.devices.append( d.to_dict() )
        return h
