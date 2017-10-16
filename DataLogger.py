import datetime
import time

from lib.Home import Home

# Configuration
minutes_between_log = 1
seconds_between_poll = 0.5

home_name = "My Intelligent Home"

# Initialize Home model
home = Home(home_name)

print(home.to_dict())

# Connect to CouchDB


# Loop forever
last_save = datetime.datetime(1999,1,1)

while True:
    print("Polling all devices")
    anything_changed = False

    # Poll all devices
    #for device in home.devices:
    #    device_status = zware.zw_api("zwep_get_if_list", "epd=" + device.device_id)
    #    print(tostring(device_status))
    #    device_basic_command_class_status = device_status.findall(".//zwif[@name='COMMAND_CLASS_BASIC']")
    #    if len(device_basic_command_class_status) == 1:
    #        print(device_basic_command_class_status)

    # Has anything changed?


    if anything_changed == True:
        # Store in CouchDB
        print("Something changed - store in CouchDB")
    else:
        # If more than
        delta = datetime.datetime.now() - last_save

        if (delta.seconds  / 60) >= minutes_between_log:
            # Store in CouchDB
            print("Peridic store in CouchDB")

            last_save = datetime.datetime.now()

    # Sleep seconds_between_poll
    time.sleep(seconds_between_poll)
