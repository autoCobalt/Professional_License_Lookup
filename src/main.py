#pre-run package installation check
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter', 'oracledb'})

#1st party pre-installed libraries
import json
import os
from typing import Final
from functools import wraps
dir_path: Final[str] = os.path.dirname(os.path.realpath(__file__))

#3rd party libraries

#custom modules
from site_search_methods import pull_site_licensing_data
from field_definitions import PharmRnSocialRecordDict, IemaLicenseRecordDict, EmtLicenseRecordDict
from excel_management import load_emplid_data
from oracle_db_requests import querydb_for_emp_data

def test_control(test_file_path: str, db_config_file_path: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("testing start")
            result = func(test_file_path, db_config_file_path, *args, **kwargs)
            print("testing end")
            return result
        return wrapper
    return decorator

@test_control(
    test_file_path=os.path.join(dir_path, 'resources', '__Test_Ref', 'emplid_license_request.xlsx'),
    db_config_file_path=os.path.join(dir_path, 'resources', '__Test_Ref', 'db_config.json')
)
def main(test_file_path: str = None, db_config_file_path: str = None) -> None:

    #load excel file emplid-license_type data
    search_list = load_emplid_data(file_path=test_file_path)

    #query database for emplid fields(name, address, for emt: last_4_ssn)
    emp_data = querydb_for_emp_data(search_list=search_list, db_config_file_path=db_config_file_path)

    #search websites based on license_type
    pulled_license_data = pull_site_licensing_data(emp_data)
    
    print(json.dumps(pulled_license_data, indent=2))
    
    
    
    # fill numeric columns with 0, convert to int, replace 0 with empty string, fill all other NaN column values with empty string
    #numeric_columns = df.select_dtypes(include=['float', 'int']).columns
    #df[numeric_columns] = df[numeric_columns].fillna(0)
    #df[numeric_columns] = df[numeric_columns].astype(int)
    #df[numeric_columns] = df[numeric_columns].replace(0, '')
    #df = df.fillna('')
    #print(df)

if __name__ == '__main__':
    main()
