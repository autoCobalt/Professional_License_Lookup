class _prop_generator(type):
    def __new__(cls, name, bases, dct):
        cls = super().__new__(cls, name, bases, dct)
        
        for prop_name in cls._PROPERTY_NAMES:
            prop = property(lambda self, prop_name=prop_name: self.__getitem__(cls._PROPERTY_FIELD_MAP[prop_name]))
            setattr(cls, prop_name, prop)
            
            prop = prop.setter(lambda self, value, prop_name=prop_name: self.__setitem__(cls._PROPERTY_FIELD_MAP[prop_name], value))
            setattr(cls, prop_name, prop)
        
        return cls