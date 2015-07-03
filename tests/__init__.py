import logging
import time
import unittest

import pyorient

from connection.connection import get_connection
from settings import test_settings
from utils import get_logger_for_name


def get_test_db_settings():
    
    settings = test_settings.ORIENT_DB_SETTINGS
    settings['db_name'] =  '%s%s' % (test_settings.ORIENT_DB_DB_NAME, str(time.time()))
    return settings


class OgormTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self._setup_db()

    def _setup_db(self):
        settings = get_test_db_settings()
        self.client = get_connection(orientdb_settings=settings)
        self.db_name = settings['db_name']
        
    def _cleanup_db(self):
        self.client.db_drop(self.db_name)

    @classmethod
    def setUpClass(cls):
        if cls is OgormTest:
            raise unittest.SkipTest("Skip OgormTest tests, it's a base class")
        super(OgormTest, cls).setUpClass()
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self._cleanup_db()
        
    def setUp(self):
        self.logger = logging.getLogger(get_logger_for_name(__name__))
        # everything after this line is embarrassing
        add_handler = True
        for h in self.logger.handlers:
            if isinstance(h, logging.StreamHandler):
                add_handler = False
        if add_handler:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
    
