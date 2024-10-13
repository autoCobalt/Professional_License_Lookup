#custom modules
from .base_license_record import BaseLicenseRecordDict

class EmtLicenseRecordDict(BaseLicenseRecordDict):
    _FIELDS = [
        "Full Name", "License Number", "License Type", "License Status", "Issue Date", "Expiration Date"
    ]
    DATEFIELDS = ["Issue Date", "Expiration Date"]
    _FIELD_CODES = ["ctl00_MainContent_lblFullName", "ctl00_MainContent_dtgLicenses_ctl02_lblFileNumber", "ctl00_MainContent_dtgLicenses_ctl02_lblObjectTypeID", "ctl00_MainContent_dtgLicenses_ctl02_Label1", "ctl00_MainContent_dtgLicenses_ctl02_Label2", "ctl00_MainContent_dtgLicenses_ctl02_Label3"]
    translate_ouput_field_to_html_name = dict(zip(_FIELDS,_FIELD_CODES))
    translate_html_name_to_output_field = dict(zip(_FIELD_CODES,_FIELDS))
    
    _PROPERTY_NAMES = [
        "full_name", "license_number", "license_type", "license_status", "issue_date", "expiration_date"
    ]
    
    _INPUT_FIELDS = ["First Name", "Last Name", "License ID", "Last 4 SSN", "Ambulance Number"]
    _INPUT_PROPERTY = ["first_name", "last_name", "license_id", "last_4_ssn", "ambulance_number"]
    translate_input_field_to_html_name= dict(zip(_INPUT_FIELDS,["ctl00$MainContent$txtFirstName", "ctl00$MainContent$txtLastName", "ctl00$MainContent$txtFileNumber", "ctl00$MainContent$txtSSN", "ctl00$MainContent$txtLicPlateNo"]))
    
    