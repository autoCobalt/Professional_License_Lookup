#custom modules
from typing import Any, Dict, override
from .base_license_record import BaseLicenseRecordDict

class IemaLicenseRecordDict(BaseLicenseRecordDict):
    _FIELDS = [
        "Name", "City", "State", "Category", "Accreditation #", "*Type", "Exp. Date"
    ]
    
    _PROPERTY_NAMES = [
        "name", "city", "state", "category", "accreditation_number", "type", "exp_date"
    ]
    
    _INPUT_FIELDS = ['lastname', 'initial', 'accred', 'Submit2']
    _INPUT_PROPERTY = _INPUT_FIELDS