#1st party pre-installed python libraries
import json
from typing import Dict, List
from datetime import datetime

#3rd party libaries
from bs4 import BeautifulSoup

#custom modules
from api_methods import get_website, post_website
from field_definitions import License_Site as lic, BaseLicenseRecordDict, EmtLicenseRecordDict, IemaLicenseRecordDict, PharmRnSocialRecordDict



#IEMA Nuclear Medicine, Radiographer, Radiation Therapy
def __search_iema(params: BaseLicenseRecordDict) -> List[Dict[str, any]]:
    records = list()

    response = post_website(lic.IEMA.base_search_url, params)
    if response and response.status_code == 200:
        table = BeautifulSoup(response.text, 'html.parser').find('table', {'class': 'dropdown'})
        if table:
            rows = table.find_all('tr')[1:]
            headers = [col.text.strip() for col in (table.find('tr')).find_all('th')]
            for row in rows:
                vals = [col.text.strip() for col in row.find_all('td')]
                record = dict(zip( headers, vals))
                records.append(record)

    return records

#IDFPR Pharmacist, Licensed Pharmacy Tech, Social Worker
def __search_idfpr(search_params: BaseLicenseRecordDict) -> List[Dict[str, any]]:
    records = list()
    params = {
        **lic.IDFPR.params,
        "q": dict(search_params)
    }
    
    response = get_website(lic.IDFPR.base_search_url, params)
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





#EMT
def __search_ems(params: BaseLicenseRecordDict) -> List[Dict[str, any]]:
    records = list()
    ifh = EmtLicenseRecordDict.translate_input_field_to_html_name
    
    response = get_website(lic.EMS.base_search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    params = { ifh[k] : v for k, v in params.items() if v and k in ifh}
    params = {
        **params,
        "__EVENTTARGET"                 : "ctl00$MainContent$btnSearch",
        "__EVENTARGUMENT"               : "",
        "ctl00$MainContent$btnSearch"   : "Submit",
        "__VIEWSTATE"                   : soup.find('input', {'name': '__VIEWSTATE'}).get('value'),
        "__EVENTVALIDATION"             : soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
    }
    

    response = post_website(lic.EMS.base_search_url, params)
    if response and response.status_code == 200:
        ofh = EmtLicenseRecordDict.translate_ouput_field_to_html_name
        soup = BeautifulSoup(response.text, 'html.parser')
        
        result_name = soup.find('span', {'id': ofh['Full Name']})
        if not result_name:
            return records
        result_name = result_name.text.strip()
        
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
                        record[hfo[col.get('id')]] = col.text.strip() if hfo[col.get('id')] not in df else datetime.strptime(col.text.strip(), "%B %d, %Y").strftime("%m/%d/%Y")
                records.append(record)

                    
    return records


def __prepare_iema(emp_rcd: Dict[str, str]) -> Dict[str, any]:
    iema_record = IemaLicenseRecordDict.get_input_fields()
    iema_record.lastname = emp_rcd['LAST_NAME_SRCH']
    iema_record.initial = emp_rcd['FIRST_NAME_SRCH'][0]
    return __search_iema(iema_record)

def __prepare_ems(emp_rcd: Dict[str, str]) -> Dict[str, any]:
    ems_record = EmtLicenseRecordDict.get_input_fields()
    ems_record.first_name = emp_rcd['FIRST_NAME_SRCH']
    ems_record.last_name = emp_rcd['LAST_NAME_SRCH']
    ems_record.last_4_ssn = emp_rcd['LAST_4_SSN']
    return __search_ems(ems_record)

def __prepare_idfpr(emp_rcd: Dict[str, str]) -> Dict[str, any]:
    idfpr_record = PharmRnSocialRecordDict.get_input_fields()
    idfpr_record.first_name = emp_rcd['FIRST_NAME_SRCH']
    idfpr_record.last_name = emp_rcd['LAST_NAME_SRCH']
    idfpr_record.license_status = 'ACTIVE'
    idfpr_record.city = emp_rcd['CITY']
    return __search_idfpr(idfpr_record)

def pull_site_licensing_data(emp_data: List[Dict[str, str]]) -> List[Dict[str, any]]:
    all_results = list()
    for emp_record in emp_data:
        #run the proper site method based on license_type. Runs the input data prep method first.
        results = request_methods[emp_record['license_type']](emp_record)
        
        for result in results:
            result['license_type'] = emp_record['license_type']
            
        all_results.extend(results)
        
    return all_results


request_methods = {
    "IDFPR": __prepare_idfpr,
    "IEMA": __prepare_iema,
    "EMS": __prepare_ems
}