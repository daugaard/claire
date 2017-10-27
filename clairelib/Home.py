import datetime
from .HomeState import HomeState

# Home object holds home name and id as well as all the devices in the home.
class Home:
    def __init__(self, name, network_service, home_id=""):
        self.network_service = network_service
        self.home_id = network_service.get_home_id()
        self.name = name
        self.devices = self.network_service.initialize_devices()

    # Updates the state of each
    def update_devices(self):
        anything_changed = False
        # Poll all devices
        for device in self.devices:
            anything_changed = anything_changed | self.network_service.update_device_state(device)

        return anything_changed

    def get_home_state(self):
        h = HomeState(home_id=self.home_id, name=self.name, time=datetime.datetime.now())
        for d in self.devices:
            h.devices.append( d.to_dict() )

        return h
