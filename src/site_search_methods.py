#1st party pre-installed python libraries
import json
from typing import Dict, List

#3rd party libaries
from bs4 import BeautifulSoup

#custom modules
from api_methods import get_website, post_website
from field_definitions import License_Site as lic, PharmRnSocialRecordDict, IemaLicenseRecordDict

def search_iema(first_name: str = None, last_name: str = None, license_nbr: str = None) -> List[Dict[str, any]]:
    
    query_params = {
        'lastname': last_name if last_name else None,
        'initial': first_name[0] if first_name else None,
        'accred': license_nbr if license_nbr else None,
        'Submit2': 'Submit'
    }

    records = list()

    response = post_website(lic.IEMA.url, query_params)
    if response and response.status_code == 200:
        table = BeautifulSoup(response.text, 'html.parser').find('table', {'class': 'dropdown'})

        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                vals = [col.text.strip() for col in row.find_all('td')]
                record = dict(zip( IemaLicenseRecordDict.get_fields(), vals))
                records.append(record)

    return records

def search_pharm(search_params: PharmRnSocialRecordDict) -> List[Dict[str, any]]:
    params = {
        **lic.PHARM_RN_SOCIAL.params,
        "q": dict(search_params)
    }
    
    records = list()
    
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