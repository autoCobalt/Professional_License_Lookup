from package_checker import check_and_install_packages
check_and_install_packages({'requests', 'bs4', 'pandas', 'openpyxl'})
from constants import License_Site

def main():
    print("this works!")
    print(License_Site.get_vals())


if __name__ == '__main__':
    main()
