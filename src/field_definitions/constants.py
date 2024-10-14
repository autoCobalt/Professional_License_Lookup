#1st party pre-installed python libraries
from enum import Enum
import logging
import re
from typing import Optional, List, Dict, Union

#3rd party libraries
from bs4 import BeautifulSoup

#custom modules
from api_methods import get_website

_LICENSE_SITES = {
    "IEMA": {
        "license_types": ["IEMA", "IEMA-NM", "IEMA-RT"],
        "url": "https://public.iema.state.il.us/iema/radiation/radtech/searchdetail.asp",
        "base_search_url": None,
        "params": None
    },
    "PHARM_RN_SOCIAL": {
        "license_types": ["LSW", "LCSW", "PHARM", "PHARMT"],
        "url": "https://data.illinois.gov/dataset/professional-licensing",
        "base_search_url": "https://data.illinois.gov/api/3/action/datastore_search",
        "params": None  # Professional Licensing site has to be dynamically determined: resource_id changes monthly
    },
    "EMT": {
        "license_types": ["EMT"],
        "url": "https://ildohemsv7prod.glsuite.us/glsuiteweb/clients/ildohems/Public/Verification/Search.aspx",
        "base_search_url": None,
        "params": None
    }
    # Add more license sites here as needed
}


class License_Site(Enum):
    IEMA  = _LICENSE_SITES["IEMA"]
    IDFPR = _LICENSE_SITES["PHARM_RN_SOCIAL"]
    EMS   = _LICENSE_SITES["EMT"]

    def __new__(cls, details: Dict[str, Union[List[str], str, Optional[Dict[str, str]]]]) -> 'License_Site':
       obj = object.__new__(cls)
       obj._value_ = details
       return obj

    @property
    def license_types(self) -> List[str]:
        return self._value_["license_types"]

    @property 
    def url(self) -> str:
        return self._value_["url"]
    
    @property 
    def base_search_url(self) -> str:
        return self._value_["base_search_url"] or self._value_["url"]

    @property
    def params(self) -> Dict[str, str]:
        return self._value_["params"] or {}

    # called at runtime to determine the resource_id of the professional license database.
    @staticmethod
    def _get_resource_id(url: str) -> Optional[str]:
        html_content = get_website(url)
        if not html_content:
            return None

        html_content = html_content.text

        #method 1 attempt to get resource_id from data-id attribute in the list item with resource-item class
        resource_item = BeautifulSoup(html_content, 'html.parser').find('li', class_= 'resource-item')
        if resource_item and 'data-id' in resource_item.attrs:
            return resource_item['data-id']
        
        #method 2 attempt to get resource_id from anything that has the data-id attribute OR
        #method 3 attempt to find anything on the page that matches the 36 alpha-numeric UUID for resource_id
        match = re.search(r'data-id="([a-f0-9-]{36})"', html_content) or re.search(r'\"id\": \"([a-f0-9-]{36})\"', html_content)
        if match:
            return match.group(1)

        logging.error("All methods failed to extract the resource ID from {url}")
        return None

License_Site.IDFPR._value_["params"] = {"resource_id": License_Site._get_resource_id(License_Site.IDFPR.url)}
