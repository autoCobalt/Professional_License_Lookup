
import json
import os
from typing import List, Dict, Final
dir_path: Final[str] = os.path.dirname(os.path.realpath(__file__))

#3rd party libraries
import oracledb
import tkinter as tk
from tkinter import filedialog

def __load_db_config(file_path: str = None) -> Dict[str, str]:
    if not file_path:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select a JSON file with DB connection details",
            filetypes=(("JSON file", "*.json"), ("", "")),
            initialdir=os.path.dirname(os.path.realpath(__file__)),
            multiple=False
        )
    if not file_path:
        raise ValueError("No file selected.")
    
    with open(file_path, "r") as config_file:
        db_config = json.load(config_file)
        
    
    # Check if all required fields are present
    required_fields = ["username", "password", "hostname", "port", "service_name"]
    for field in required_fields:
        if field not in db_config:
            raise ValueError(f"Missing field '{field}' in the JSON file.")
    
    return db_config

def __load_sql_query(file_path: str) -> str:
    with open(file_path, "r") as sql_file:
        return sql_file.read().strip().rstrip(";")

def querydb_for_emp_data(search_list: List[Dict[str, str]], db_config_file_path: str = None) -> List[Dict[str, str]]:
    # Define the directory

    # Define sql_file_path, then load the sql file, then
    # Replace the placeholder with the actual emplid_list
    sql_file_path = os.path.join(dir_path, 'resources', 'query_for_emp_info.sql')
    sql_query = __load_sql_query(sql_file_path)
    sql_query = sql_query.replace("&emplid_list", ",".join([f"'{record['emplid']}'" for record in search_list]))


    # Define temporary db_config file path, then
    # Load the DB configuration data
    db_config = __load_db_config(db_config_file_path)
    
    ds = f"{db_config["hostname"]}:{db_config["port"]}/{db_config["service_name"]}"
    
    results = []
    cursor = None
    try:
        with oracledb.connect(user=db_config['username'], password=db_config['password'], dsn=ds) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)

            result_column_names = [h[0] for h in cursor.description]
            result_column_names.insert(1, 'license_type')
            ssn_4_index = result_column_names.index('LAST_4_SSN')

            for row in cursor:
                emplid = row[0]
                licenses_to_find = [emplid_license for emplid_license in search_list if emplid_license['emplid'] == emplid]
                for license_row in licenses_to_find:
                    license_type = license_row['license_type']
                    result_row = list(row)
                    result_row.insert(1, license_type)
                    if license_type != 'EMS':
                        result_row[ssn_4_index] = ''
                    results.append(dict(zip(result_column_names, result_row)))
            
            cursor.close()
    except oracledb.Error as error:
        print(f"Error connecting to the database: {error}")
    
    return results