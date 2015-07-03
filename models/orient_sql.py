import logging

from connection.connection import get_connection
from models.fields import to_java_case
from utils import get_logger_for_name


logger = logging.getLogger(get_logger_for_name(__name__))


def create_class(klass, extends=None, client=None):
    
    if client is None:
        client = get_connection()
    
    class_name = klass.__name__
    
    create_str = 'CREATE CLASS %s' % class_name
    
    if extends is not None:
        create_str  =  '%s EXTENDS %s' % (create_str, extends)
    
    c = klass()
        
    logger.debug("creating class with command %s" % create_str)

    client.command(create_str)
    
    for k in c._fields:
        field_str = 'CREATE PROPERTY %s.%s %s' % (class_name, to_java_case(k), c._fields[k].orientdb_type)
        logger.debug("applying property with command %s" % (field_str))
        client.command(field_str)
