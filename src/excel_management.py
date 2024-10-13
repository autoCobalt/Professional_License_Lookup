import tkinter as tk
from tkinter import filedialog
from typing import Union

# 3rd party libraries
import pandas as pd

def __select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Excel/CSV file",
        filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"))
    )
    return file_path

def read_excel_file(file_path: Union[str, None] = None) -> pd.DataFrame:
    if file_path is None:
        file_path = __select_file()
    # Read the file
    return pd.read_excel(file_path, sheet_name=0)