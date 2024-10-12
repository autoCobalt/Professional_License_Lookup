#custom modules
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})
from site_search_methods import search_pharm, search_iema
from field_definitions import LicenseRecordDict

#1st party pre-installed libraries
import json

def main() -> None:

    #print(json.dumps(search_pharm('Divya'), indent=2))
    #print(json.dumps(search_iema("Davis"), indent=2))
    #print(json.dumps(search_iema(license_nbr="500479871"), indent=2))
    print("testing blank")
    lic = LicenseRecordDict()
    print(json.dumps(lic, indent=2))
    print(lic.get_empty_dict())
    print(lic.get_fields())
    
    
    lic["Description"] = "pharmzzz"
    lic.description = "pharm"
    print(lic.description)
    print(lic["Description"])

if __name__ == '__main__':
    main()
