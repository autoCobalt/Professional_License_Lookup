import sys
import subprocess
import importlib
from typing import Set, Final

def __install(package: str) -> None:
    try:
        print(f"<<<<<< installing: {package} >>>>>>")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. You might need to run this script with administrator privileges.")
        sys.exit(1)

def __is_package_installed(package_name: str) -> bool:
    try:
        importlib.import_module(package_name)
        return True   
    except ImportError:
        return False

def check_and_install_packages(modules: str) -> None:
    missing: Set[str] = {package for package in modules if not __is_package_installed(package)}

    if missing:
        print(f"Installing missing libraries... {missing}")
        for package in missing:
            __install(package)
        print("<<<<<< All required packages have been installed. Continuing... >>>>>>")
