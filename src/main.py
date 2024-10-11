#custom modules
from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})
from site_search_methods import search_pharm, search_iema

#1st party pre-installed libraries
from constants import License_Site
from typing import Optional, List, Union
import json

def main() -> None:

    #print(json.dumps(search_pharm('Divya'), indent=2))
    print(json.dumps(search_iema('Chad',"Davis"), indent=2))


if __name__ == '__main__':
    main()
