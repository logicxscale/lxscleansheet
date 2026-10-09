import pandas as pd

def detect_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)

def get_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.duplicated(keep=False)]
