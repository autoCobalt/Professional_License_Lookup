from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})


from constants import License_Site
from typing import Optional, List

from site_search_methods import search_pharm


def main() -> None:
    print("testing...")

    search_pharm('Gina', 'Puig', 'Chicago')

if __name__ == '__main__':
    main()
