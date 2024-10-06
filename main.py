from package_checker import check_and_install_packages
check_and_install_packages({'requests', 'bs4', 'pandas', 'openpyxl'})


def main():
    print("this works!")


if __name__ == '__main__':
    main()