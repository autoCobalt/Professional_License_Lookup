#1st party pre-installed python libraries
import json
from typing import Dict, List
from datetime import datetime

#3rd party libaries
from bs4 import BeautifulSoup

#custom modules
from api_methods import get_website, post_website
from field_definitions import License_Site as lic, PharmRnSocialRecordDict, IemaLicenseRecordDict, BaseLicenseRecordDict, EmtLicenseRecordDict

def search_iema(params: BaseLicenseRecordDict) -> List[Dict[str, any]]:
    records = list()

    response = post_website(lic.IEMA.base_search_url, params)
    if response and response.status_code == 200:
        table = BeautifulSoup(response.text, 'html.parser').find('table', {'class': 'dropdown'})

        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                vals = [col.text.strip() for col in row.find_all('td')]
                record = dict(zip( IemaLicenseRecordDict.get_fields(), vals))
                records.append(record)

    return records

def search_pharm(search_params: BaseLicenseRecordDict) -> List[Dict[str, any]]:
    records = list()
    params = {
        **lic.PHARM_RN_SOCIAL.params,
        "q": dict(search_params)
    }
    
    response = get_website(lic.PHARM_RN_SOCIAL.base_search_url, params)
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

def search_emt(params: BaseLicenseRecordDict) -> List[Dict[str, any]]:
    records = list()
    ifh = EmtLicenseRecordDict.translate_input_field_to_html_name
    
    response = get_website(lic.EMT.base_search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    params = { ifh[k] : v for k, v in params.items() if v}
    params = {
        **params,
        "__EVENTTARGET"                 : "ctl00$MainContent$btnSearch",
        "__EVENTARGUMENT"               : "",
        "ctl00$MainContent$btnSearch"   : "Submit",
        "__VIEWSTATE"                   : soup.find('input', {'name': '__VIEWSTATE'}).get('value'),
        "__EVENTVALIDATION"             : soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
    }
    

    response = post_website(lic.EMT.base_search_url, params)
    if response and response.status_code == 200:
        ofh = EmtLicenseRecordDict.translate_ouput_field_to_html_name
        soup = BeautifulSoup(response.text, 'html.parser')
        
        result_name = soup.find('span', {'id': ofh['Full Name']}).text.strip()
        table = BeautifulSoup(response.text, 'html.parser').find('table', {'id': 'ctl00_MainContent_dtgLicenses'})
        
        if table:
            hfo = EmtLicenseRecordDict.translate_html_name_to_output_field
            rows = table.find_all('tr')
            for row in rows:
                record = EmtLicenseRecordDict.get_empty_dict()
                record["Full Name"] = result_name
                td_elements = row.find_all('td')
                cols = [span for td in td_elements for span in td.find_all('span', id=True)]
                df = EmtLicenseRecordDict.DATEFIELDS
                for col in cols:
                    if hfo[col.get('id')] in record:
                        record[hfo[col.get('id')]] = col.text.strip() if hfo[col.get('id')] not in df else datetime.strptime(col.text.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
                records.append(record)

                    
    return records