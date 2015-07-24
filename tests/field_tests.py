import random

from arrow.arrow import Arrow

from models.exceptions import ValidationError
from models.fields import Field, IntegerField, FloatField, StringField, \
    DateTimeField, BinaryField, to_java_case, BooleanField
from tests import OgormTest


class TestBasicFields(OgormTest):
    
    def test__validate_minimum_value(self):
        
        field = Field(minimum_value=10)
        field.value = 5
        self.assertRaises(ValidationError, field._validate_minimum_value)
        
    def test__validate_not_null(self):
        
        field = Field(not_null=True)
        self.assertRaises(ValidationError, field._validate_not_null)
        
    def test__validate_maximum_value(self):
        
        field = Field(maximum_value=10)
        field.value = 15
        self.assertRaises(ValidationError, field._validate_maximum_value)
        
    def test_default_gets_set(self):
        
        field = Field(default=10)
        self.assertEqual(field.value, 10)
        
    def test_to_java_case(self):
        
        self.assertEqual(to_java_case("COnvert_this_to_java_case"), "convertThisToJavaCase")
        

class TestIntegerField(OgormTest):
    
    def test_type_validation(self):
        
        field = IntegerField()
        field.value = 'f'
        self.assertRaises(ValidationError, field._type_validation)
        field.value = random.randint(1,5)
        field._type_validation()
        
    
class TestFloatField(OgormTest):
    
    def test_type_validation(self):
        
        field = FloatField()
        field.value = 'f'
        self.assertRaises(ValidationError, field._type_validation)
        field.value = random.random()
        field._type_validation()
        
        
class TestStringField(OgormTest):

    def test_type_validation(self):
        
        field = StringField()
        field.value = 10
        self.assertRaises(ValidationError, field._type_validation)
        field.value = 'foobar'
        field._type_validation()


class TestDateTimeField(OgormTest):
    
    def test_type_validation(self):
        
        field = DateTimeField()
        field.value = 'f'
        self.assertRaises(ValidationError, field._type_validation)
        field.value = Arrow.utcnow()
        field._type_validation()


class TestBinaryField(OgormTest):
    
    def test_type_validation(self):
        
        field = BinaryField()
        field.value = 'f'
        self.assertRaises(ValidationError, field._type_validation)
        field.value = bytes(range(20))
        field._type_validation()

class TestBooleanField(OgormTest):
    
    def test_type_validation(self):
        
        field = BooleanField()
        field.value = 'f'
        self.assertRaises(ValidationError, field._type_validation)
        field.value = True
        field._type_validation()
        field.value = False
        field._type_validation()