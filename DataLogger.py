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

    # Has anything changed?
    anything_changed = home.update_devices()

    if anything_changed == True:
        # Store in CouchDB
        print("Something changed - store in CouchDB")
        print(home.to_dict())

    else:
        # If more than
        delta = datetime.datetime.now() - last_save

        if (delta.seconds  / 60) >= minutes_between_log:
            # Store in CouchDB
            print("Peridic store in CouchDB")
            print(home.to_dict())

            last_save = datetime.datetime.now()

    # Sleep seconds_between_poll
    time.sleep(seconds_between_poll)
