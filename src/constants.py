from enum import Enum
from typing import Optional, List
import logging
import re
import requests
from bs4 import BeautifulSoup



class LicenseType_Site(Enum):
    
    IEMA: str = "https://public.iema.state.il.us/iema/radiation/radtech/radtechsearch.asp"
    PHARM_RN_SOCIAL: str = None # Professional Licensing site has to be dynamically determined: resource_id changes monthly
    EMT: str = "https://ildohemsv7prod.glsuite.us/glsuiteweb/clients/ildohems/Public/Verification/Search.aspx"



    @property
    def value(self):
        # Determine resource_id for professional licensing site.
        if self.name == 'PHARM_RN_SOCIAL':
            return LicenseType_Site.__get_resource_id("https://data.illinois.gov/dataset/professional-licensing", "https://data.illinois.gov/api/3/action/datastore_search")
        return super().value

    @staticmethod
    def get_vals() -> List[str]:
        return [col.value for col in LicenseType_Site]

    @staticmethod
    def __get_webpage_content(url: str) -> Optional[str]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch webpage: {e}")
            return None

    @staticmethod
    def __method_1_beautifulsoup(html_content: str) -> Optional[str]:
        soup = BeautifulSoup(html_content, 'html.parser')
        resource_item = soup.find('li', class_= 'resource-item')
        if resource_item and 'data-id' in resource_item.attrs:
            return resource_item['data-id']
        return None

    @staticmethod
    def __method_2_regex(html_content: str) -> Optional[str]:
        pattern = r'data-id="([a-f0-9-]{36})"'
        match = re.search(pattern, html_content)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def __method_3_javascript(html_content: str) -> Optional[str]:
        pattern = r'\"id\": \"([a-f0-9-]{36})\"'
        match = re.search(pattern, html_content)
        if match:
            return match.group(1)
        return None

    # called at runtime to determine the resource_id of the professional license database.
    @staticmethod
    def __get_resource_id(url: str, base_url: str) -> Optional[str]:
        html_content = LicenseType_Site.__get_webpage_content(url)
    
        if not html_content:
            logging.error("Failed to retrieve webpage content.")
            return None
    
        methods = [
            ("BeautifulSoup", LicenseType_Site.__method_1_beautifulsoup),
            ("Regex", LicenseType_Site.__method_2_regex),
            ("JavaScript", LicenseType_Site.__method_3_javascript)
        ]
    
        for method_name, method_func in methods:
            resource_id = method_func(html_content)
            if resource_id:
                return f"{base_url}?resource_id={resource_id}"
            else:
                logging.warning(f"{method_name} method failed to extract resource ID.")
    
        logging.error("All methods failed to extract the resource ID.")
        return None
