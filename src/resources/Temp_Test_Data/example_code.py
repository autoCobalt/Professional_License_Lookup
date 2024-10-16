#pre-run package installation check
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter', 'oracledb', 'customtkinter'})

#1st party pre-installed libraries
import json
import os
from typing import Final
dir_path: Final[str] = os.path.dirname(os.path.realpath(__file__))

#3rd party libraries
import pandas as pd
import customtkinter as ctk

#custom modules
from site_search_methods import request_methods, pull_site_licensing_data
from field_definitions import PharmRnSocialRecordDict, IemaLicenseRecordDict, EmtLicenseRecordDict
from excel_management import load_emplid_data
from oracle_db_requests import querydb_for_emp_data
from functools import wraps

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

def show_login_window():
    def on_submit():
        nonlocal username, password
        username = entry_username.get()
        password = entry_password.get()
        login_window.destroy()

    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry("400x300")

    ctk.CTkLabel(login_window, text="Login", font=("Arial", 24)).pack(pady=20)

    ctk.CTkLabel(login_window, text="Username").pack(pady=5)
    entry_username = ctk.CTkEntry(login_window)
    entry_username.pack(pady=5)

    ctk.CTkLabel(login_window, text="Password").pack(pady=5)
    entry_password = ctk.CTkEntry(login_window, show="*")
    entry_password.pack(pady=5)

    ctk.CTkButton(login_window, text="Submit", command=on_submit).pack(pady=20)

    username = None
    password = None
    login_window.mainloop()

    return username, password

@test_control(
    test_file_path=os.path.join(dir_path, 'resources', '__Test_Ref', 'emplid_license_request.xlsx'),
    db_config_file_path=os.path.join(dir_path, 'resources', '__Test_Ref', 'db_config.json')
)
def main(test_file_path: str, db_config_file_path: str) -> None:
    # Show login window to get username and password
    username, password = show_login_window()

    # Load excel file emplid-license_type data
    search_list = load_emplid_data(file_path=test_file_path)

    # Query database for emplid fields (name, address, for emt: last_4_ssn)
    emp_data = querydb_for_emp_data(search_list=search_list, db_config_file_path=db_config_file_path)

    # Search websites based on license_type
    pull_site_licensing_data(emp_data)

if __name__ == "__main__":
    main()