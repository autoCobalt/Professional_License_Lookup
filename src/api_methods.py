import logging
import os
import requests
from typing import Optional, Dict, Union, List
import urllib.parse

def get_website(url: str, params: Union[Dict[str, str], None] = None) -> Optional[str]:
        try:
            full_url = url
            if params:
                encoded_params = urllib.parse.urlencode(params, quote_via = urllib.parse.quote)
                full_url = f"{url}?{encoded_params}"

            response = requests.get(full_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch webpage: {e}")
            return None

# No current use case as a standalone script.
def main():
    print(f"{os.path.basename(__file__)} is not a standalone script.")

if __name__ == '__main__':
    main()
