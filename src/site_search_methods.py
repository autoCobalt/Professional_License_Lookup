import json
import os
from typing import List, Optional
import urllib.parse


from constants import License_Site as lic
from api_methods import get_website

def search_iema(first_name: str, last_name: str) -> Optional[List]:
    params = {
        'lastname': last_name,
        'initial': first_name[0] if first_name else '',
        'Submit2': 'Submit'
    }

def search_pharm(first_name: str, last_name: str, city: str):
    query_params = {
        'First Name': first_name.upper(),
        'Last Name': last_name.upper(),
        'City': city.upper(),
        'License Status': 'ACTIVE'
    }

    params = {
        **lic.PHARM_RN_SOCIAL.params,
        "q": json.dumps(query_params)
    }

    

    print(get_website(lic.PHARM_RN_SOCIAL.url, params))

# No current use case as a standalone script.
def main():
    print(f"{os.path.basename(__file__)} is not a standalone script.")

if __name__ == '__main__':
    main()