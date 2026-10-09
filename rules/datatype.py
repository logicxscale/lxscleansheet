import pandas as pd
import re

DATE_PATTERNS = [
    r"\d{2}/\d{2}/\d{4}",
    r"\d{4}-\d{2}-\d{2}",
    r"\d{2}-\d{2}-\d{4}",
]

CURRENCY_SYMBOLS = ["$", "Rp", "€", "£", "¥", "USD", "IDR", "EUR"]

def normalize_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    return df.convert_dtypes()

def detect_date_columns(df: pd.DataFrame) -> list:
    date_cols = []
    for col in df.select_dtypes(include=['object', 'string']):
        sample = df[col].dropna().astype(str).head(20)
        matches = sum(
            any(re.match(p, v) for p in DATE_PATTERNS)
            for v in sample
        )
        if matches > len(sample) * 0.5:
            date_cols.append(col)
    return date_cols

def normalize_dates(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df_clean = df.copy()
    for col in cols:
        try:
            df_clean[col] = pd.to_datetime(df_clean[col], infer_format=True, errors='coerce')
        except Exception:
            pass
    return df_clean

def detect_currency_columns(df: pd.DataFrame) -> list:
    curr_cols = []
    exclude_keywords = ['id', 'code', 'telp', 'phone', 'postal', 'zip', 'tahun', 'year', 'nik', 'npwp', 'number', 'no']
    for col in df.select_dtypes(include=['object', 'string']):
        col_lower = col.lower()
        if any(kw in col_lower for kw in exclude_keywords):
            continue
        sample = df[col].dropna().astype(str).head(20)
        if len(sample) == 0:
            continue
        has_currency_symbol = any(
            any(sym in v for sym in CURRENCY_SYMBOLS)
            for v in sample
        )
        if has_currency_symbol:
            curr_cols.append(col)
    return curr_cols

def normalize_currency(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df_clean = df.copy()
    for col in cols:
        df_clean[col] = (
            df_clean[col]
            .astype(str)
            .str.replace(r"[^\d.]", "", regex=True)
        )
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    return df_clean
