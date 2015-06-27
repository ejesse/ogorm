import datetime

from models.exceptions import ValidationError


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
            
    def _set_python_type(self):
        self.python_type = None
    
    def _validate_not_null(self):
        if self.not_null:
            if self.value is None:
                raise ValidationError("Value is None, but self.not_null is True")
    
    def _validate_minimum_value(self):
        if self.minimum_value is not None:
            if self.value < self.minimum_value:
                raise ValidationError("Value %s is less than minimum value %s" % (self.value, self.minimum_value))
            
    def _validate_maximum_value(self):
        if self.maximum_value is not None:
            if self.value > self.maximum_value:
                raise ValidationError("Value %s is greater than maximum value %s" % (self.value, self.maximum_value))
    
    def validate(self):
        pass
    
    def _type_validation(self):
        if self.value is not None:
            if not isinstance(self.value, self.python_type):
                raise ValidationError("%s is not a valid value for %s" % (self.value, self.__class__.__name__))
    
    def _basic_validation(self):
        self._validate_not_null()
        self._type_validation()
        self._validate_minimum_value()
        self._validate_maximum_value()
        self.validate()
        

class IntegerField(Field):
    
    def _set_python_type(self):
        self.python_type = int
    

class FloatField(Field):

    def _set_python_type(self):
        self.python_type = float


class StringField(Field):
    
    def _set_python_type(self):
        self.python_type = str


class DateTimeField(Field):
    
    def _set_python_type(self):
        self.python_type = datetime.datetime


class BinaryField(Field):
    
    def _set_python_type(self):
        self.python_type = bytes
