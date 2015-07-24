import base64

import arrow
from arrow.arrow import Arrow

from models.exceptions import ValidationError


def to_java_case(string_to_convert):
    
    components = string_to_convert.lower().split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])
    

class Field:

    def __init__(self, minimum_value=None, 
                 maximum_value=None,
                 mandatory=False,
                 readonly=False,
                 not_null=False,
                 unique=False,
                 regexp=None,
                 default=None):
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.mandatory = mandatory
        self.readonly = readonly
        self.not_null = not_null
        self.unique = unique
        self.regexp = regexp
        self.value = None
        if default is not None:
            self.value = default
        self._set_python_type()
        self._set_orientdb_type()
        self._set_orientdb_type_id()
        self.inherited = False
        
    def clean_value(self, value):
        return value
        
    def orient_value(self):
        return self.value
    
    def to_json(self):
        return repr(self)
    
    def orient_to_python(self, value):
        self.value = value
            
    def _set_python_type(self):
        self.python_type = None
        
    def _set_orientdb_type(self):
        self.orientdb_type = None
        
    def _set_orientdb_type_id(self):
        self.orientdb_type_id = None
    
    def _validate_not_null(self):
        if self.not_null:
            if self.value is None:
                raise ValidationError(
                      "Value is None, but self.not_null is True")
    
    def _validate_minimum_value(self):
        if self.minimum_value is not None:
            if self.value < self.minimum_value:
                raise ValidationError(
                  "Value %s is less than minimum value %s" % (self.value, 
                                                          self.minimum_value))
            
    def _validate_maximum_value(self):
        if self.maximum_value is not None:
            if self.value > self.maximum_value:
                raise ValidationError(
                  "Value %s is greater than maximum value %s" % (self.value, 
                                                         self.maximum_value))
    
    def validate(self):
        pass
    
    def _type_validation(self):
        if self.value is not None:
            if not isinstance(self.value, self.python_type):
                raise ValidationError(
                  "%s is not a valid value for %s" % (self.value, 
                                                      self.__class__.__name__))
    
    def _basic_validation(self):
        self._validate_not_null()
        self._type_validation()
        self._validate_minimum_value()
        self._validate_maximum_value()
        self.validate()
        

class IntegerField(Field):
    
    def _set_python_type(self):
        self.python_type = int
        
    def _set_orientdb_type(self):
        self.orientdb_type = 'integer'
        
    def _set_orientdb_type_id(self):
        self.orientdb_type_id = 1
    

class FloatField(Field):

    def _set_python_type(self):
        self.python_type = float

    def _set_orientdb_type(self):
        self.orientdb_type = 'float'
        
    def _set_orientdb_type_id(self):
        self.orientdb_type_id = 4


class StringField(Field):
    
    def _set_python_type(self):
        self.python_type = str

    def _set_orientdb_type(self):
        self.orientdb_type = 'string'
        
    def _set_orientdb_type_id(self):
        self.orientdb_type_id = 7


class DateTimeField(Field):
    
    def _set_python_type(self):
        self.python_type = Arrow

    def _set_orientdb_type(self):
        self.orientdb_type = 'long'
        
    def _set_orientdb_type_id(self):
        self.orientdb_type_id = 4
        
    def to_json(self):
        if self.value is not None:
            return str(self.value)
        return None
    
    def orient_value(self):
        # trying to use timezones with the driver
        # and orient is a nightmare
        # let's just ensure we go to UTC
        # before we save and then do it naive
        if self.value is not None:
            # first make sure it's UTC
            ovalue = self.value.to('utc')
            return ovalue.timestamp
        return None
        
    def orient_to_python(self, value):
        # we get back a float from orient
        # convert it to a utc Arrow time object
        pvalue = arrow.get(value)
        self.value = pvalue.to('utc')
    
    def clean_value(self, value):
        if value is not None:
            return arrow.get(value.format('YYYY-MM-DD HH:mm:ssZ'))
    

class BinaryField(Field):
    
    def _set_python_type(self):
        self.python_type = bytes

    def _set_orientdb_type(self):
        self.orientdb_type = 'binary'
        
    def _set_orientdb_type_id(self):
        self.orientdb_type_id = 8
        
    def orient_value(self):
        #we're saving via json, so let's base64 it
        if self.value is not None:
            return base64.b64encode(self.value).decode()
        return None
    
    def orient_to_python(self, value):
        # UN base64 it
        if value is not None:
            self.value = base64.b64decode(value.encode())
        
