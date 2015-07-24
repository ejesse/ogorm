from models.base import Model
from models.model_utils import get_orient_valid_class_name


def is_model(klass):
    if hasattr(klass,'__call__'):
        klass = klass()
    return isinstance(klass, Model)


def get_model_extensions(klass):
    extensions = []
    if not hasattr(klass,'__call__'):
        klass = klass.__class__
    if not isinstance(klass(), Model):
        raise ValueError("This method only examines Model and extending classes or instances")
    if not klass.__base__ is Model:
        for extender in klass.__bases__:
            extensions.append(get_orient_valid_class_name(extender))
    return extensions