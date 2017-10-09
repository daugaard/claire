import datetime
import time

# Configuration
minutes_between_log = 1
seconds_between_poll = 0.5

# Connect to Z-Wave

# Get all devices

# Initialize Home model

# Connect to CouchDB


# Loop forever
last_save = datetime.datetime(1999,1,1)

while True:
    print "Polling all devices"
    anything_changed = False

    # Poll all devices

    # Has anything changed?


    if anything_changed == True:
        # Store in CouchDB
        print "Something changed - store in CouchDB"
    else:
        # If more than
        delta = datetime.datetime.now() - last_save

        if (delta.seconds  / 60) >= minutes_between_log:
            # Store in CouchDB
            print "Peridic store in CouchDB"

            last_save = datetime.datetime.now()

    # Sleep seconds_between_poll
    time.sleep(seconds_between_poll)
