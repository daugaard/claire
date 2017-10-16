from . import zware
from .BasicDevice import BasicDevice

from xml.etree.ElementTree import tostring

zware_address = "https://raspberrypi.local/"
zware_user = "sigma"
zware_password = "sigmadesigns"

class NetworkService():
    def __init__(self):
        # Connect to Z-Wave
        r = zware.zw_init(zware_address,zware_user,zware_password)
        v = r.findall("./version")[0]
        print("Connected to zware version: " + v.get('app_major') + '.' + v.get('app_minor'))

    def initialize_devices(self):

        devices = []

        # Get all devices
        print("Retrieving all nodes from the ZIP Gateway through ZWare")

        # Get all nodes
        rn = zware.zw_api("zwnet_get_node_list")
        print(tostring(rn))
        nodes = rn.findall("./zwnet/zwnode")
        for node in nodes:
            print("Getting node " + node.get("desc"))
            # For each node get all endpoints
            endpoints_request = zware.zw_api("zwnode_get_ep_list", "noded=" + node.get('desc'))
            # Most devices will only have one endpoint, but lets iterate through just in case
            endpoints = endpoints_request.findall("./zwnode/zwep")
            for endpoint in endpoints:
                print(tostring(endpoint))
                print("Found endpoint device with id: " + endpoint.get('desc') + " called " + endpoint.get('name') + " in " + endpoint.get("loc"))
                # Create device
                device = BasicDevice( endpoint.get('desc'), endpoint.get('name'), 0 )
                devices.append(device)

        return devices
