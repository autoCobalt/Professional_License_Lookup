#pre-run package installation check
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})

#1st party pre-installed libraries
import json

#3rd party libraries
import pandas as pd

#custom modules
from site_search_methods import search_pharm, search_iema, search_emt
from field_definitions import PharmRnSocialRecordDict, IemaLicenseRecordDict, EmtLicenseRecordDict
from excel_management import read_excel_file

def main() -> None:
    print("testing start")
    
    #params = PharmRnSocialRecordDict.get_input_fields()
    #params.first_name = "Connie"
    #params.last_name = "Davis"

    #print(json.dumps(search_pharm(params), indent=2))
    #print(json.dumps(search_iema(first_name="Connie",last_name="Davis"), indent=2))
    #iema_lic = IemaLicenseRecordDict.get_input_fields()
    #print(iema_lic)
    #iema_lic.accred = "500521409"
    #print(json.dumps(search_iema(iema_lic), indent=2))
    #print(iema_lic)
    #iema_lic['accred'] = "500479871"
    #print(json.dumps(search_iema(iema_lic), indent=2))
    #print(iema_lic)
    
    emt_input = EmtLicenseRecordDict.get_input_fields()
    emt_input.first_name = "Grace"
    emt_input.last_name = "Lee"
    emt_input.license_id = "060821907"
    print(json.dumps(search_emt(emt_input), indent=2))
    #print(json.dumps(search_emt(emt_input), indent=2))
    
    #print(json.dumps(lic, indent=2))
    
    
    #lic["Description"] = "pharmzzz"
    #lic.description = "pharm"
    #print(lic.description)
    #print(lic["Description"])
    
    df = read_excel_file()
    print(df)
    
    print("testing end")

if __name__ == '__main__':
    main()
