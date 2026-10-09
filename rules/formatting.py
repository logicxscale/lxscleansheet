import pandas as pd

def format_text_value(x):
    if isinstance(x, str):
        s = x.strip()
        if not s:
            return s
        if '@' in s or 'http://' in s or 'https://' in s:
            return s
        if s.isupper() and any(c.isalpha() for c in s):
            return s.title()
        return s
    return x

def normalize_text_case(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.select_dtypes(include=['object', 'string']):
        df_clean[col] = df_clean[col].apply(format_text_value)
    return df_clean

def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.select_dtypes(include=['object', 'string']):
        df_clean[col] = df_clean[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df_clean
