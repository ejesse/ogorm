import logging
import time
import unittest

import pyorient

from utils import get_logger_for_name


db_name = 'ogorm-test-db'
username = 'root'
password = 'root'
host = 'localhost'
port = 2424


class OgormTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.db_name = '%s%s' % (db_name, str(time.time()))
        self._setup_db()

    def _setup_db(self):
        client = pyorient.OrientDB(host, port)
        session_id = client.connect(username, password)
        client.db_create(self.db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
        
    def _cleanup_db(self):
        client = pyorient.OrientDB(host, port)
        session_id = client.connect(username, password)
        client.db_drop(self.db_name)

    @classmethod
    def setUpClass(cls):
        if cls is OgormTest:
            raise unittest.SkipTest("Skip OgormTest tests, it's a base class")
        super(OgormTest, cls).setUpClass()
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self._cleanup_db()
        
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.client = pyorient.OrientDB(host, port)
        session_id = self.client.connect(username, password)
        self.client.db_open(self.db_name, username, password)
        self.logger = logging.getLogger(get_logger_for_name(__name__))
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
    
