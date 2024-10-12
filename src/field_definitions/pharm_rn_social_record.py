#1st party pre-installed python libraries
from typing import Dict, Any, List

#custom modules
from .base_license_record import BaseLicenseRecordDict

class PharmRnSocialRecordDict(BaseLicenseRecordDict):
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