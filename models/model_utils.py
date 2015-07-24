import importlib


def get_full_class_path_name(obj):
    if hasattr(obj,'__call__'):
        obj = obj()
    return obj.__module__ + "." + obj.__class__.__name__


def get_orient_valid_class_name(obj):
    name = get_full_class_path_name(obj)
    return name.replace(".", "___dot___")


def get_module_class_name_from_orient_class_name(orient_class):
    pythonized = orient_class.replace("___dot___", ".")
    parts = pythonized.split(".")
    class_name = parts.pop()
    module_name = '.'.join(parts)
    return module_name, class_name


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    module = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    klass = getattr(module, class_name)
    return klass


def get_class_from_orient_class_name(orient_class):
    # wraps up other functions into one
    module_name, class_name = get_module_class_name_from_orient_class_name(
                                                                   orient_class)
    return class_for_name(module_name, class_name)
