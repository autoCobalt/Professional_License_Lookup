#1st party pre-installed libraries
import logging
import os
from typing import Optional, Dict, Union, List

#3rd party libraries *from the requests installation*
import requests

def get_website(url: str, search_params: Union[Dict[str, str], None] = None) -> Optional[requests.Response]:
    return __check_status(requests.get(url, params=search_params))

def post_website(url: str, params: Union[Dict[str, str], None] = None) -> Optional[requests.Response]:
    return __check_status(requests.post(url, data=params))

def __check_status(req_response: requests.Response) -> Optional[requests.Response]:
    try:
        req_response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed call to webpage: {e}")

    return req_response
    

# No current use case as a standalone script.
def main():
    print(f"{os.path.basename(__file__)} is not a standalone script.")

if __name__ == '__main__':
    main()
