import json
import logging

from connection.connection import get_connection
from models.models import get_orient_valid_class_name
from utils import get_logger_for_name


LOGGER = logging.getLogger(get_logger_for_name(__name__))


def create_class(klass, extends=None, client=None):
    
    if client is None:
        client = get_connection()
    
    class_name = get_orient_valid_class_name(klass)
    
    create_str = 'CREATE CLASS %s' % class_name
    
    if extends is not None:
        create_str  =  '%s EXTENDS %s' % (create_str, extends)
    
    instance = klass()
        
    LOGGER.debug("creating class with command %s" % create_str)

    client.command(create_str)
    
    for k in instance._fields.keys():
        field_str = 'CREATE PROPERTY %s.%s %s' % (class_name, 
                                      instance._py_to_orient_field_mapping[k], 
                                      instance._fields[k].orientdb_type)
        LOGGER.debug("applying property with command %s" % (field_str))
        client.command(field_str)


def insert(obj, client=None):
    
    if client is None:
        client = get_connection()
        
    class_name = get_orient_valid_class_name(obj)
    
    insert_str = "INSERT INTO %s" % class_name
    
    values = {}
    
    for k in obj._fields.keys():
        values[obj._py_to_orient_field_mapping[k]] = obj._fields[k].value

             
    insert_str = "%s CONTENT %s" % (insert_str, json.dumps(values))
    resp = client.command(insert_str)
    rec = resp[0]
    obj.rid = rec._rid
    return rec

def load(rid, client=None):
    
    if client is None:
        client = get_connection()
        
    return client.record_load(rid)
    