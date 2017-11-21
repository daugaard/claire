import couchdb
from couchdb.design import ViewDefinition

views = []

views.append( ViewDefinition('home_state','by_time', '''function(doc) {
        emit(doc.time, doc);
}''') )

views.append( ViewDefinition('home_state','by_name', '''function(doc) {
        emit(doc.name, doc);
}''') )


def sync(database):
    couchdb.design.ViewDefinition.sync_many(database, views, remove_missing=True)
