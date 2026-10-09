from utils.excel import load_excel
import pandas as pd

def read_data(file) -> pd.DataFrame:
    return load_excel(file)
