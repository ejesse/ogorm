import json
import logging

from connection.connection import get_connection
from models.model_utils import get_orient_valid_class_name
from utils import get_logger_for_name


LOGGER = logging.getLogger(get_logger_for_name(__name__))


def create_class(klass, client=None):
    from models.orient_sql_utils import is_model
    from models.orient_sql_utils import get_model_extensions
    if not is_model(klass):
        raise ValueError("Only OrientDB models can be used to create Orient classes")
    
    if client is None:
        client = get_connection()
    
    class_name = get_orient_valid_class_name(klass)
    
    create_str = 'CREATE CLASS %s' % class_name
    
    parents = get_model_extensions(klass)
    
    if len(parents) > 0:
        if len(parents) > 1:
            extenders = ",".join(parents)
        else:
            extenders = parents[0]
        create_str  =  '%s EXTENDS %s' % (create_str, extenders)
    
    instance = klass()
        
    LOGGER.debug("creating class with command %s" % create_str)

    client.command(create_str)
    
    for k in instance._fields.keys():
        if not instance._fields[k].inherited:
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
        values[obj._py_to_orient_field_mapping[k]] = obj._fields[k].orient_value()

    insert_str = "%s CONTENT %s" % (insert_str, json.dumps(values))
    LOGGER.debug("executing insert command: %s" % insert_str)
    resp = client.command(insert_str)
    rec = resp[0]
    obj.rid = rec._rid
    return rec


def load(rid, client=None):
    
    if client is None:
        client = get_connection()
        
    return client.record_load(rid)


def update(obj, client=None):
    
    if client is None:
        client = get_connection()
        
    class_name = get_orient_valid_class_name(obj)
    
    update_str = "UPDATE %s " % class_name
    
    values = {}
    
    for k in obj._fields.keys():
        values[obj._py_to_orient_field_mapping[k]] = obj._fields[k].orient_value()

    update_str = "%s CONTENT %s" % (update_str, json.dumps(values))
    resp = client.command(update_str)
    rec = resp[0]
    return rec
    