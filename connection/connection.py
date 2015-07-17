import pyorient

import settings


def get_connection(orientdb_settings=
                   settings.OgormSettings().ORIENT_DB_SETTINGS):
    
    client = pyorient.OrientDB(orientdb_settings['host'], 
                               orientdb_settings['port'])
    client.connect(orientdb_settings['username'], orientdb_settings['password'])
    if not client.db_exists(orientdb_settings['db_name']):
        client.db_create(orientdb_settings['db_name'], 
                         orientdb_settings['db_type'], 
                         orientdb_settings['db_storage'])
    client.db_open(orientdb_settings['db_name'], 
                   orientdb_settings['username'], 
                   orientdb_settings['password'])
    return client
    