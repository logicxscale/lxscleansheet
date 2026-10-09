import pandas as pd
from rules.formatting import trim_whitespace

def detect_duplicates(df: pd.DataFrame) -> int:
    if df is None or df.empty:
        return 0
    df_clean = trim_whitespace(df)
    return int(df_clean.duplicated().sum())

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    df_clean = trim_whitespace(df)
    return df_clean.drop_duplicates().reset_index(drop=True)

def get_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df.iloc[0:0]
    df_clean = trim_whitespace(df)
    dup_mask = df_clean.duplicated(keep=False)
    return df[dup_mask]
