import pandas as pd
import io

def load_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)

def save_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='CleanedData')
    return output.getvalue()
