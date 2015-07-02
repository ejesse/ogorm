import pyorient


#defaults
ORIENT_DB_USERNAME = 'root'
ORIENT_DB_PASSWORD = 'root'
ORIENT_DB_HOST = 'localhost'
ORIENT_DB_PORT = 2424
ORIENT_DB_DB_NAME = 'default'
ORIENT_DB_NAME = ORIENT_DB_DB_NAME
ORIENT_DB_DB_TYPE = pyorient.DB_TYPE_GRAPH
ORIENT_DB_TYPE = ORIENT_DB_DB_TYPE
ORIENT_DB_DB_STORAGE_TYPE = pyorient.STORAGE_TYPE_MEMORY
ORIENT_DB_STORAGE_TYPE = ORIENT_DB_DB_STORAGE_TYPE

ORIENT_DB_SETTINGS = {'username': ORIENT_DB_USERNAME,
                      'password': ORIENT_DB_PASSWORD,
                      'host': ORIENT_DB_HOST,
                      'port': ORIENT_DB_PORT,
                      'db_name': ORIENT_DB_DB_NAME,
                      'db_type': ORIENT_DB_DB_TYPE,
                      'db_storage': ORIENT_DB_DB_STORAGE_TYPE
                      }