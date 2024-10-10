from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})


from constants import License_Site
from typing import Optional, List

def search_iema(first_name: str, last_name: str) -> Optional[List]:
    params = {
        'lastname': last_name,
        'initial': first_name[0] if first_name else '',
        'Submit2': 'Submit'
    }


def main() -> None:
    print("testing...")
    for site in License_Site:
        print('\n',site.name, site.url, site.params,site.value, sep='\n')

if __name__ == '__main__':
    main()
