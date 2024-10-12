from typing import Dict, Any
from .base_license_record import BaseLicenseRecordDict

class IemaLicenseRecordDict(BaseLicenseRecordDict):
    _FIELDS = [
        "Name", "City", "State", "Category", "Accreditation #", "*Type", "Exp. Date"
    ]
    
    _PROPERTY_NAMES = [
        "name", "city", "state", "category", "accreditation_number", "type", "exp_date"
    ]