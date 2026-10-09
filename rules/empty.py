import pandas as pd

def detect_empty_cells(df: pd.DataFrame) -> int:
    df_temp = df.copy()
    for col in df_temp.select_dtypes(include=['object', 'string']):
        df_temp[col] = df_temp[col].replace(r'^\s*$', pd.NA, regex=True)
    return int(df_temp.isnull().sum().sum())

def fill_empty_cells(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.select_dtypes(include=['object', 'string']):
        df_clean[col] = df_clean[col].replace(r'^\s*$', pd.NA, regex=True)
    for col in df_clean.columns:
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].fillna(0)
        else:
            df_clean[col] = df_clean[col].fillna('Unknown')
    return df_clean

def detect_empty_columns(df: pd.DataFrame) -> list:
    df_temp = df.copy()
    for col in df_temp.select_dtypes(include=['object', 'string']):
        df_temp[col] = df_temp[col].replace(r'^\s*$', pd.NA, regex=True)
    return df_temp.columns[df_temp.isnull().all()].tolist()

def drop_empty_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    return df.drop(columns=cols)

def get_empty_cells_rows(df: pd.DataFrame) -> pd.DataFrame:
    df_temp = df.copy()
    for col in df_temp.select_dtypes(include=['object', 'string']):
        df_temp[col] = df_temp[col].replace(r'^\s*$', pd.NA, regex=True)
    return df_temp[df_temp.isnull().any(axis=1)]
