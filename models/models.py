from models.fields import Field, to_java_case


class ModelBase(type):
    
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        
        if abstract:
            # Abstract base models can't be instantiated and don't appear in
            # the list of models for an app. We do the final setup for them a
            # little differently from normal models.
            attr_meta.abstract = False
            new_class.Meta = attr_meta
            return new_class
        
        # setup field container
        setattr(new_class, '_field_defs', {})
        
        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            if isinstance(obj, Field):
                new_class._field_defs[obj_name]= obj
            setattr(new_class, obj_name, obj)
            
        return new_class
    
 
class Model(metaclass=ModelBase):
    
    def __init__(self, *args, **kwargs):
        self._fields = {}
        self._py_to_orient_field_mapping = {}
        self._instantiate_fields()
            
    def _instantiate_fields(self):
        # read through the fields in the class variable
        # and assign new instances to their attribute names
        for k in self._field_defs.keys():
            # we'll need a way to bypass our get/set fancy/schmancy
            # so put copies of the fields in _fields
            self._fields[k] = self._field_defs[k].__class__.__call__()
            super(Model, self).__setattr__(k, self._fields[k])
            # setup the field mapping
            self._py_to_orient_field_mapping[k] = to_java_case(k)
            # in both directions
            # note: it works fine if they are the same!
            self._py_to_orient_field_mapping[to_java_case(k)] = k 
            
    def __getattribute__(self, name):
        val = super(Model, self).__getattribute__(name)
        if isinstance(val, Field):
            return val.value
        return val
    
    def __setattr__(self, name, value):
        try:
            attr = super(Model, self).__getattribute__(name)
            if isinstance(attr, Field):
                attr.value = value
            else:
                super(Model, self).__setattr__(name, value)
        except AttributeError:
            super(Model, self).__setattr__(name, value)
