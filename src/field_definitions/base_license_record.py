from typing import Dict, Any, List
from .prop_generator import prop_generator

class BaseLicenseRecordDict(dict, metaclass=prop_generator):
    _FIELDS = []
    _PROPERTY_NAMES = []
    _PROPERTY_FIELD_MAP = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__class__._PROPERTY_FIELD_MAP is None:
            self.__class__._initialize_property_field_map()
        self._initialize_attributes()

    @classmethod
    def _initialize_property_field_map(cls):
        cls._PROPERTY_FIELD_MAP = {prop: field for prop, field in zip(cls._PROPERTY_NAMES, cls._FIELDS)}


    def _initialize_attributes(self):
        for field in self._FIELDS:
            if field not in self:
                self[field] = None

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in self._PROPERTY_FIELD_MAP:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        self[self._PROPERTY_FIELD_MAP[name]] = value
            
    def __setitem__(self, key: str, value: Any) -> None:
        if key not in self._FIELDS:
            raise KeyError(f"Invalid key: {key}")
        super().__setitem__(key, value)
        
    @classmethod
    def get_fields(cls) -> List[str]:
        return cls._FIELDS.copy()
    
    @classmethod
    def get_empty_dict(cls) -> Dict[str, Any]:
        return {field: None for field in cls._FIELDS}