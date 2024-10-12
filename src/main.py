#custom modules
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})
from site_search_methods import search_pharm, search_iema
from field_definitions import LicenseRecordDict

#1st party pre-installed libraries
import json

def main() -> None:
    print("testing start")
    
    params = LicenseRecordDict()
    params.first_name = "Divya"
    params.last_name = "Gandhi"
    params.license_status = "Active"

    print(json.dumps(search_pharm(params), indent=2))
    print(json.dumps(search_iema(first_name="Chad",last_name="Davis"), indent=2))
    print(json.dumps(search_iema(license_nbr="500479871"), indent=2))
    
    #lic = LicenseRecordDict()
    #print(json.dumps(lic, indent=2))
    #print(lic.get_empty_dict())
    #print(lic.get_fields())
    
    
    #lic["Description"] = "pharmzzz"
    #lic.description = "pharm"
    #print(lic.description)
    #print(lic["Description"])
    json.dumps(search_pharm(params), indent=2)
    print("testing end")

if __name__ == '__main__':
    main()
