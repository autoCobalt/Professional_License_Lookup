#1st party pre-installed libraries
import logging
import os
import tkinter as tk
from tkinter import filedialog
from typing import Union

# 3rd party libraries
import pandas as pd

def __select_file(dir_path: str = None):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Excel/CSV file",
        filetypes=(("Excel or CSV file", "*.xlsx *.csv"), ("", "")),
        initialdir=dir_path,
        multiple=False
    )
    return file_path

def read_excel_file(file_path: Union[str, None] = None, dir_path: str = None) -> pd.DataFrame:
    if file_path is None:
        file_path = __select_file(dir_path=dir_path)
    if file_path is None:
        raise ValueError("No file selected.")
    extension_type = os.path.splitext(file_path)[1]
    # Read the file
    try:
        if extension_type == '.xlsx':
            return pd.read_excel(file_path)
        elif extension_type == '.csv':
            return pd.read_csv(file_path)
        else:
            raise ValueError(f"File extension type ({extension_type}) is neither xlsx nor csv.")
    except FileNotFoundError as e:
        logging.error(f"File not found. {e}")