from utils.excel import save_excel
import pandas as pd

def export_data(df: pd.DataFrame) -> bytes:
    return save_excel(df)
