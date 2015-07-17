import logging

from models.fields import StringField
from models.models import Model
from tests import OgormTest


class TestModels(OgormTest):
    
    def test_create_a_basic_class(self):
        cluster_id = self.client.command( "create class my_class extends V" )
        r = self.client.command("insert into my_class ( 'accommodation', 'work', 'holiday' ) values( 'B&B', 'garage', 'mountain' )")
        
    def test_basic_instantiation(self):
        
        class TestModel1(Model):
            pass
        
        class TestModel2(TestModel1):
            pass
        
        self.assertTrue(isinstance(TestModel2(), TestModel1))
        self.assertTrue(isinstance(TestModel2(), Model))
        
    def test_field_accessor(self):
        
        class TestModel1(Model):
            foo = StringField()
        
        # we do two here to make sure they assigned as instance vars
        # instead of class vars
            
        m = TestModel1()
        m.foo = 'bar'
        
        m2 = TestModel1()
        m2.foo = 'barbar'
        
        self.assertEqual(m.foo,'bar')
        self.assertEqual(m._fields['foo'].value,'bar')
        self.assertEqual(m2.foo,'barbar')
        self.assertEqual(m2._fields['foo'].value,'barbar')
        
        # make sure normal accessors still work
        
        m.normal = 123
        m2.normal = 456
        
        self.assertEqual(m.normal, 123)
        self.assertEqual(m2.normal, 456)
    
        self.assertFalse('normal' in m._fields)
        self.assertFalse('normal' in m2._fields)
        
    def test_record_id_handling(self):
        
        class TestRid(Model):
            foo = StringField()
        
        test_cluster_id = 4
        test_cluster_position = 12
        test_rid = '#%s:%s' % (test_cluster_id, test_cluster_position)
        
        trid = TestRid()
        self.assertIsNone(trid.rid)
        self.assertIsNone(trid.cluster_id)
        self.assertIsNone(trid.cluster_position)
        trid.rid = test_rid
        # basic test
        self.assertEqual(trid.rid, test_rid)
        # test the cluster ID
        self.assertEqual(trid.cluster_id, test_cluster_id)
        # test the cluster position
        self.assertEqual(trid.cluster_position, test_cluster_position)
        
        # test some oops cases
        self.assertRaises(ValueError, trid._set_rid, 'fjdksfjdksl')
        self.assertRaises(ValueError, trid._set_rid, '#fjdks:fjdksl')
        self.assertRaises(ValueError, trid._set_rid, '#4:fjdksl')
        self.assertRaises(ValueError, trid._set_rid, '#fjdks:12')
        
        trid.rid = test_rid.replace('#', '')
        self.assertEqual(trid.rid, test_rid)
        
