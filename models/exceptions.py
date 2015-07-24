class OgormError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    

class ValidationError(OgormError):
    pass

class ReadOnlyError(OgormError):
    pass
