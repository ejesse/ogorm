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
        