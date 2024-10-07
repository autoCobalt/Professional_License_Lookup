from package_checker import install_required_libraries
install_required_libraries({'requests', 'bs4', 'pandas', 'openpyxl','xlsxwriter'})
from constants import License_Site

def main():
    print("this works!\n")
    print(*License_Site.get_vals(), sep='\n')


if __name__ == '__main__':
    main()
