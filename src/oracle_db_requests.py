
import json
import os
from typing import List, Dict


#3rd party libraries
import oracledb
import tkinter as tk
from tkinter import filedialog

def load_db_config() -> Dict[str, str]:
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

def load_sql_query(file_path: str) -> str:
    with open(file_path, "r") as sql_file:
        return sql_file.read().strip().rstrip(";")

def querydb_for_emp_data(search_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # Define the path to the SQL file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sql_file_path = os.path.join(dir_path, 'resources', 'query_for_emp_info.sql')
    
    sql_query = load_sql_query(sql_file_path)
    
    # Replace the placeholder with the actual emplid_list
    sql_query = sql_query.replace("&emplid_list", ",".join([f"'{record['emplid']}'" for record in search_list]))
    
    # Load the DB configuration
    db_config = load_db_config()  
    username = db_config["username"]
    password = db_config["password"]
    hostname = db_config["hostname"]
    port = db_config["port"]
    service_name = db_config["service_name"]
    

    ds = f"{hostname}:{port}/{service_name}"
    
    
    
    results = []
    try:
        with oracledb.connect(user=username, password=password, dsn=ds) as connection:
            print("Successfully connected to the database")
          
            with connection.cursor() as cursor:
                
                cursor.execute(sql_query)
                results = cursor.fetchall()
                cursor.close()
                print(f"Query returned {len(results)} rows")
                print(results)
    except oracledb.Error as error:
        if error.code == 1017:
            print("Error 1017: Please check your credentials.")
        else:  
            print(f"Error connecting to the database: {error}")
    finally:
        if connection:
            connection.close()
        print("Database connection closed")
    return results