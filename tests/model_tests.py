import logging

from models.fields import StringField
from models.models import Model, get_full_class_path_name, \
    get_orient_valid_class_name, get_module_class_name_from_orient_class_name, \
    class_for_name, get_class_from_orient_class_name
from models.orient_sql import load, create_class, insert
from tests import OgormTest
from tests.orient_sql_tests import ClassToInsert


class TestModels(OgormTest):
    
    def test_get_full_class_path_name(self):
        self.assertEqual(get_full_class_path_name(ClassToInsert), "tests.orient_sql_tests.ClassToInsert")
        self.assertEqual(get_full_class_path_name(ClassToInsert()), "tests.orient_sql_tests.ClassToInsert")
        
    def test_get_orient_valid_class_name(self):
        self.assertEqual(get_orient_valid_class_name(ClassToInsert), "tests___dot___orient_sql_tests___dot___ClassToInsert")
        self.assertEqual(get_orient_valid_class_name(ClassToInsert()), "tests___dot___orient_sql_tests___dot___ClassToInsert")
        
    def test_get_module_class_name_from_orient_class_name(self):
        module, class_name = get_module_class_name_from_orient_class_name("tests___dot___orient_sql_tests___dot___ClassToInsert")
        self.assertEqual(module, 'tests.orient_sql_tests')
        self.assertEqual(class_name, 'ClassToInsert')
    
    def test_create_a_basic_class(self):
        self.client.command( "create class my_class extends V" )
        self.client.command("insert into my_class ( 'accommodation', 'work', 'holiday' ) values( 'B&B', 'garage', 'mountain' )")
         
    def test_class_for_name(self):
        module, class_name = get_module_class_name_from_orient_class_name("tests___dot___orient_sql_tests___dot___ClassToInsert")
        klass = class_for_name(module, class_name)
        self.assertEqual(klass, ClassToInsert)
        
    def test_get_class_from_orient_class_name(self):
        # test the whole above shebang wrapper
        klass = get_class_from_orient_class_name(get_orient_valid_class_name(ClassToInsert))
        self.assertEqual(klass, ClassToInsert)
        klass = get_class_from_orient_class_name(get_orient_valid_class_name(ClassToInsert()))
        self.assertEqual(klass, ClassToInsert)
            
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
        
    def test_from_orient(self):
        
        create_class(ClassToInsert, client=self.client)
        
        class_to_insert = ClassToInsert()
        class_to_insert.int_field = 10
        class_to_insert.str_field = 'foobar'
        insert(class_to_insert, client=self.client)
        r = load(class_to_insert.rid, client=self.client)
        result = Model.from_orient(r)
        self.assertEqual(class_to_insert.__class__, result.__class__)
        self.assertEqual(result.rid, class_to_insert.rid)
        self.assertEqual(result.str_field, class_to_insert.str_field)
        self.assertEqual(result.int_field, class_to_insert.int_field)
