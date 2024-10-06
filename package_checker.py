import sys
import subprocess
import importlib
from typing import Set, Final

def _install(package: str) -> None:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. You might need to run this script with administrator privileges.")
        sys.exit(1)

def _is_package_installed(package_name: str) -> bool:
    try:
        importlib.import_module(package_name)
        return True   
    except ImportError:
        return False

def check_and_install_packages(modules: str) -> None:
    missing: Set[str] = {package for package in modules if not _is_package_installed(package)}

    if missing:
        print("Installing missing libraries...")
        for package in missing:
            _install(package)
        print("All required packages have been installed.")
    else:
        print("All required packages are already installed.")