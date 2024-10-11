
#1st party pre-installed libraries
import logging
import os
from typing import Optional, Dict, Union, List

#3rd party libraries *from the requests installation*
import requests
import urllib.parse

def get_website(url: str, search_params: Union[Dict[str, str], None] = None) -> Optional[requests.Response]:
    response = None
    try:
        full_url = f"{url}?{urllib.parse.urlencode(search_params, quote_via = urllib.parse.quote)}" if search_params else url

        response = requests.get(full_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch webpage: {e}")

    return response

def post_website(url: str, params: Union[Dict[str, str], None] = None) -> Optional[requests.Response]:
    response = None
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to post webpage: {e}")

    return response

# No current use case as a standalone script.
def main():
    print(f"{os.path.basename(__file__)} is not a standalone script.")

if __name__ == '__main__':
    main()
