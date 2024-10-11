#1st party pre-installed python libraries
from enum import Enum
import logging
import os
import re
from typing import Optional, List, Dict, Tuple, Union

#3rd party libraries
from bs4 import BeautifulSoup

#custom modules
from api_methods import get_website




class License_Site(Enum):
    
    IEMA:           Tuple[List[str],str, Union[Dict[str, str], None]] = (["IEMA","IEMA-NM","IEMA-RT"],"https://public.iema.state.il.us/iema/radiation/radtech/searchdetail.asp", None)
    PHARM_RN_SOCIAL:Tuple[List[str],str, Union[Dict[str, str], None]] = (["LSW","LCSW","PHARM","PHARMT"],"https://data.illinois.gov/dataset/professional-licensing", None) # Professional Licensing site has to be dynamically determined: resource_id changes monthly
    EMT:            Tuple[List[str],str, Union[Dict[str, str], None]] = (["EMT"],"https://ildohemsv7prod.glsuite.us/glsuiteweb/clients/ildohems/Public/Verification/Search.aspx", None) 

    def __new__(cls, lic_type: List[str], url: str, params: Union[Dict[str, str], None]):
       obj = object.__new__(cls)
       obj._value_ = (lic_type, url, params)
       return obj

    @property
    def license_types(self) -> List[str]:
        return self._value_[0]

    @property 
    def url(self) -> str:
        return self._value_[1]

    @property
    def params(self) -> Dict[str, str]:
        return self._value_[2] or {}

    # called at runtime to determine the resource_id of the professional license database.
    @staticmethod
    def _get_resource_id(base_url: str) -> Optional[str]:
        html_content = get_website(License_Site.PHARM_RN_SOCIAL.url)
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

License_Site.PHARM_RN_SOCIAL._value_ = (License_Site.PHARM_RN_SOCIAL._value_[0], "https://data.illinois.gov/api/3/action/datastore_search", {"resource_id": License_Site._get_resource_id("https://data.illinois.gov/api/3/action/datastore_search")})

# No current use case as a standalone script.
def main() -> None:
    print(f"{os.path.basename(__file__)} is not a standalone script.")

if __name__ == '__main__':
    main()
