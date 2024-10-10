import logging
import os
import requests
from typing import Optional

def get_website(url: str) -> Optional[str]:
        try:
            response = requests.get(url)
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
