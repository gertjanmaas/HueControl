
class HueLight(object):
    def __init__(self):
        self._on = None
        self._bri = None
        self._type = None
        self._hue = None
        self._sat = None
        self._xy = None
        self._ct = None
        self.colormode = None
        self.reachable = True
        self.name = ""
        self.modelid = ""
        self.number = 0
        
    @property
    def on(self):
        return self._on
    
    @on.setter
    def on(self, value):
        if not isinstance(value, bool):
            if value.lower() in ['true', '1']:
                self._on = True
            else:
                self._on = False
        else:
            self._on = value
    
    @property
    def bri(self):
        return self._bri
    
    @bri.setter
    def bri(self, value):
            self._bri = int(value)
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
            self._type = value
            
    @property
    def hue(self):
        return self._hue
    
    @hue.setter
    def hue(self, value):
            self._hue = int(value)
            
    @property
    def sat(self):
        return self._sat
    
    @sat.setter
    def sat(self, value):
            self._sat = int(value)
            
    @property
    def xy(self):
        return self._x
    
    @xy.setter
    def xy(self, value):
            self._x = value
            
    @property
    def ct(self):
        return self._ct
    
    @ct.setter
    def ct(self, value):
            self._ct = int(value)    
            