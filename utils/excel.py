import pandas as pd
import io

def get_excel_sheets(file) -> list:
    try:
        excel_file = pd.ExcelFile(file)
        sheets = excel_file.sheet_names
        if hasattr(file, 'seek'):
            file.seek(0)
        return sheets
    except Exception:
        if hasattr(file, 'seek'):
            file.seek(0)
        return [0]

def load_excel(file, sheet_name=0) -> pd.DataFrame:
    try:
        df = pd.read_excel(file, sheet_name=sheet_name)
        if hasattr(file, 'seek'):
            file.seek(0)
        return df
    except Exception as e:
        if hasattr(file, 'seek'):
            file.seek(0)
        raise e

def save_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='CleanedData')
    return output.getvalue()
