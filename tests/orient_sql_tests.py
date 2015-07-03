import logging

from models import models
from models.fields import Field, IntegerField, FloatField, StringField, \
    DateTimeField, BinaryField, to_java_case
from models.orient_sql import create_class
from tests import OgormTest
from utils import get_logger_for_name


class TestModels(OgormTest):
    
    def test_basic_class_creation(self):
        
        cluster_id = self.client.command( "create class my_class extends V" )
        r = self.client.command("insert into my_class ( 'accommodation', 'work', 'holiday' ) values( 'B&B', 'garage', 'mountain' )")
        self.assertEqual(r[0]._OrientRecord__rid, self.client.record_load(r[0]._OrientRecord__rid)._OrientRecord__rid)
        
    def test_create_class(self):
        
        class Foo(models.Model):
            pass
        
        create_class(Foo, client=self.client)
        
        r = self.client.command("select expand(classes) from metadata:schema")
        
        # we are making sure that the class is defined in Orient
        # by looping through all the defined classes and looking
        # for Foo
        self.assertTrue(any(x.name == Foo.__name__ for x in r))
            
    def test_create_class_with_attribues(self):
        
        class ClassWithAttributes(models.Model):
            
            str_field = StringField()
            int_field = IntegerField()
            float_field = FloatField()
            datetime_field = DateTimeField()
            bin_field = BinaryField()
            
        create_class(ClassWithAttributes, client=self.client)
        
        # we will get the properties and make sure they are
        # correct types and names
        r = self.client.command("select expand(properties) from ( select expand(classes) from metadata:schema) where name = '%s'" % ClassWithAttributes.__name__)
        cwa = ClassWithAttributes()
        for f in cwa._fields.keys():
            self.assertTrue(any(x.type == cwa._fields[f].orientdb_type_id for x in r))
            self.assertTrue(any(x.name == to_java_case(f) for x in r))
        

