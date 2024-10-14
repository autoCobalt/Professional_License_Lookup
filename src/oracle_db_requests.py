import oracledb
import os

def 

NETWORK_FOLDER = r"P:\DatastoreFOLDER"

script_dir = os.path.dirname(os.path.abspath(__file__))
sql_file_path = os.path.join(script_dir, "ps_nurse_list_names.sql")


usename = "enter_later"
pasword = "pwd_later"
hostname = "hostname.com"
port = 1234
service_name = "SRVCNME"

ds = f"{hostname}:{port}/{service_name}"

try:
    with oracledb.connect(user=usename, password=pasword, dsn=ds) as connection:
        print("Successfully connected to the database")
      
        with connection.cursor() as cursor:
            sql_query = ""
            
            with open(sql_file_path,"r") as sql_file:
              sql_query = sql_file.read().strip().rstrip(";")
            
    
            cursor.execute(sql_query)
    
            for row in cursor:
                print(row)
  
except oracledb.Error as error:
    print(f"Error connecting to the database: {error}")

print("Database connection closed")