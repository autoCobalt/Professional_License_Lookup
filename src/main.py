#pre-run package installation check
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter', 'oracledb'})

#1st party pre-installed libraries
import json
import os
from typing import Final
dir_path: Final[str] = os.path.dirname(os.path.realpath(__file__))

#3rd party libraries
import pandas as pd

#custom modules
from site_search_methods import request_methods, pull_site_licensing_data
from field_definitions import PharmRnSocialRecordDict, IemaLicenseRecordDict, EmtLicenseRecordDict
from excel_management import load_emplid_data
from oracle_db_requests import querydb_for_emp_data

def main() -> None:
    print("testing start")
    #test files
    test_file_path = os.path.join(dir_path, 'resources', '_Test_Ref', 'emplid_license_request.xlsx')
    db_config_file_path = os.path.join(dir_path, 'resources', '_Test_Ref', 'db_config.json')

    
    #test_idfpr()
    #test_ems()
    #test_iema()
    
    search_list = load_emplid_data(file_path=test_file_path)
    emp_data = querydb_for_emp_data(search_list=search_list, db_config_file_path=db_config_file_path)
    pull_site_licensing_data(emp_data)
    
    
    
    
    #df = read_excel_file(dir_path=dir_path)
    
    # fill numeric columns with 0, convert to int, replace 0 with empty string, fill all other NaN column values with empty string
    #numeric_columns = df.select_dtypes(include=['float', 'int']).columns
    #df[numeric_columns] = df[numeric_columns].fillna(0)
    #df[numeric_columns] = df[numeric_columns].astype(int)
    #df[numeric_columns] = df[numeric_columns].replace(0, '')
    #df = df.fillna('')
    #print(df)
    
    
    print("testing end")

def test_idfpr():
    #testing IDFPR site search (RN, Physician, Social Worker)
    params = PharmRnSocialRecordDict.get_input_fields()
    params.first_name = "Connie"
    params.last_name = "Davis"
    params.license_type = "PHARMACY"
    print(json.dumps(request_methods['IDFPR'](params), indent=2))
    
def test_iema():
    #testing IEMA site search (Nuclear Medicine, Radiographer)
    iema_lic = IemaLicenseRecordDict.get_input_fields()
    iema_lic.accred = "500521409"
    print(json.dumps(request_methods['IEMA'](iema_lic), indent=2))
    iema_lic['accred'] = "500479871"
    print(json.dumps(request_methods['IEMA'](iema_lic), indent=2))

def test_ems():
    #testing EMS site search (EMT)
    emt_input = EmtLicenseRecordDict.get_input_fields()
    emt_input.first_name = "Grace"
    emt_input.last_name = "Lee"
    emt_input.license_id = "060821907"
    print(json.dumps(request_methods['EMS'](emt_input), indent=2))

if __name__ == '__main__':
    main()
