#1st party pre-installed python libraries
import json
import os
from typing import Dict, List, Optional, Union

#3rd party libaries
from constants import License_Site as lic
from api_methods import get_website, post_website
from bs4 import BeautifulSoup

def search_iema(first_name: str, last_name: str) -> Optional[List[Dict[str, any]]]:
    
    query_params = {
        'lastname': last_name,
        'initial': first_name[0] if first_name else '',
        'Submit2': 'Submit'
    }

    records: List[Dict[str, any]] = []

    response = post_website(lic.IEMA.url, query_params)
    if response and response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Caused by searching: {query_params}")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'dropdown'})

        if table:
            rows = table.find_all('tr')[1:]
            headers =  table.find_all('th')
            k_values = []
            for header in headers:
                k_values.append(header.text.strip())

            for row in rows:
                cols = row.find_all('td')
                v_values = []
                for col in cols:
                    v_values.append(col.text.strip())

                records.append(dict(zip(k_values, v_values)))

    return records
    

def search_pharm(first_name: Union[str, None] = None, last_name: Union[str, None] = None, city: Union[str, None] = None) -> Optional[List[Dict[str, any]]]:
    query_params = {
        'First Name': first_name.upper() if first_name else None,
        'Last Name': last_name.upper() if last_name else None,
        'City': city.upper() if city else None,
        'License Status': 'ACTIVE'
    }
    params = {
        **lic.PHARM_RN_SOCIAL.params,
        "q": json.dumps({k: v for k, v in query_params.items() if v})
    }
    
    records: List[Dict[str, any]] = []
    
    response = get_website(lic.PHARM_RN_SOCIAL.url, params)
    if response and response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Caused by searching: {query_params}")
    else:
        try:
            data = response.json()
            records = data["result"]["records"]
            if not records:
                print(f"No records found for: {query_params}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")

    return records
    

# No current use case as a standalone script.
def main():
    print(f"{os.path.basename(__file__)} is not a standalone script.")

if __name__ == '__main__':
    main()