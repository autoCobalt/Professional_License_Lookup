#1st party pre-installed python libraries
import json
import os
from typing import Dict, List, Union

#3rd party libaries
from bs4 import BeautifulSoup

#custom modules
from api_methods import get_website, post_website
from field_definitions import License_Site as lic, LicenseRecordDict

def search_iema(first_name: str = None, last_name: str = None, license_nbr: str = None) -> List[Dict[str, any]]:
    
    query_params = {
        'lastname': last_name if last_name else None,
        'initial': first_name[0] if first_name else None,
        'accred': license_nbr if license_nbr else None,
        'Submit2': 'Submit'
    }

    records: List[Dict[str, any]] = list()

    response = post_website(lic.IEMA.url, query_params)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'dropdown'})

        if table:
            rows = table.find_all('tr')[1:]
            headers =  table.find_all('th')
            k_values = list()
            for header in headers:
                k_values.append(header.text.strip())

            for row in rows:
                cols = row.find_all('td')
                v_values = list()
                for col in cols:
                    v_values.append(col.text.strip())

                record = dict(zip(k_values, v_values))
                records.append(record)

    return records
    

def search_pharm(search_params: LicenseRecordDict) -> List[Dict[str, any]]:
    params = {
        **lic.PHARM_RN_SOCIAL.params,
        "q": dict(search_params)
    }
    
    records: List[Dict[str, any]] = list()
    
    response = get_website(lic.PHARM_RN_SOCIAL.url, params)
    if response and response.status_code == 200:
        try:
            data = response.json()
            records = data["result"]["records"]
            if not records:
                print(f"No records found for: {search_params}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")

    return records