import configparser
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import Element

from clairelib.NetworkService import NetworkService

config = configparser.ConfigParser()
config.read('config.cfg')

zware_address = config.get("ZWare", "zware_address")
zware_user = config.get("ZWare", "zware_user")
zware_password = config.get("ZWare", "zware_password")

n = NetworkService(zware_address, zware_user, zware_password)

devices = n.initialize_devices()
dids = []
for device in devices:
    dids.append(device.device_id)

while True:
    for device in devices:
        print("Device ID: " + device.device_id + " Device Name: " + device.name )

    did = input("Enter device id (or q to quit): ")
    if did == 'q':
        exit()
    if did in dids:

        command_classes = n.get_command_classes(did)
        i = 0
        for command_class in command_classes:
            print(str(i) + ": " + command_class)
            i += 1

        endpoint_i = int(input("Enter command class endpoint: "))
        command_class = command_classes[endpoint_i]

        command = input("Enter Z-Wave command name (e.g. sensor): ")
        number = int(input("Enter command Numer (e.g. 2): "))
        args = input("Enter command args (e.g. &unit=2): ")

        r = n.send_command(did, command_class, command, number, args)

        if type(r) is Element:
            print(tostring(r))
        else:
            print(r)

    else:
        print("Unknown device id")
