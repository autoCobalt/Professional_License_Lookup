from typing import Dict, Any, List
from ._prop_generator import _prop_generator


class LicenseRecordDict(dict, metaclass=_prop_generator):
    _FIELDS = [
        "_id", "License Type", "Description", "License Number", "License Status",
        "Business", "Title", "First Name", "Middle", "Last Name", "Prefix", "Suffix",
        "Business Name", "BusinessDBA", "Original Issue Date", "Effective Date",
        "Expiration Date", "City", "State", "Zip", "County", "Specialty/Qualifier",
        "Controlled Substance Schedule", "Delegated Controlled Substance Schedule",
        "Ever Disciplined", "LastModifiedDate", "Case Number", "Action",
        "Discipline Start Date", "Discipline End Date", "Discipline Reason", "rank"
    ]
    
    _PROPERTY_NAMES = [
        "id", "license_type", "description", "license_number", "license_status",
        "business", "title", "first_name", "middle", "last_name", "prefix", "suffix",
        "business_name", "business_dba", "original_issue_date", "effective_date",
        "expiration_date", "city", "state", "zip", "county", "specialty_qualifier",
        "controlled_substance_schedule", "delegated_controlled_substance_schedule",
        "ever_disciplined", "last_modified_date", "case_number", "action",
        "discipline_start_date", "discipline_end_date", "discipline_reason", "rank"
    ]
    
    _PROPERTY_FIELD_MAP = {prop: field for prop, field in zip(_PROPERTY_NAMES, _FIELDS)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize_attributes()

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
