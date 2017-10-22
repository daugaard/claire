# A state representation at the home at a specific time.
# This class is based on the CouchDB document class to allow for it to be easily stored and retrieved.

from couchdb.mapping import Document, TextField, IntegerField, BooleanField, DateTimeField, ListField, DictField

class HomeState(Document):
    home_id = TextField()
    name = TextField()
    time = DateTimeField()
    periodic_update = BooleanField()
    devices = ListField(DictField())
