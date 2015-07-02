from settings import default_settings


class Borg:
    
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state
        


class OgormSettings(Borg):
    
    def __init__(self, settings=None, *args, **kwargs):
        super(OgormSettings, self).__init__(*args, **kwargs)
        if settings is None:
            settings = default_settings
        for item in dir(settings):
            if not item.startswith("__"):
                self.__dict__[item] = settings.__dict__[item]             
    