from utils.excel import load_excel, get_excel_sheets
import pandas as pd

def read_data(file, sheet_name=0) -> pd.DataFrame:
    return load_excel(file, sheet_name=sheet_name)
