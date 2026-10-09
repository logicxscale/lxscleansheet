import pandas as pd

def detect_empty_cells(df: pd.DataFrame) -> int:
    return int(df.isnull().sum().sum())

def fill_empty_cells(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.columns:
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].fillna(0)
        else:
            df_clean[col] = df_clean[col].fillna('Unknown')
    return df_clean

def detect_empty_columns(df: pd.DataFrame) -> list:
    return df.columns[df.isnull().all()].tolist()

def drop_empty_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    return df.drop(columns=cols)

def get_empty_cells_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.isnull().any(axis=1)]
