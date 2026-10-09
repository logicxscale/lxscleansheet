from rules.empty import detect_empty_cells, detect_empty_columns
from rules.duplicate import detect_duplicates
from rules.datatype import detect_date_columns, detect_currency_columns
from rules.typo import detect_typos_fuzzy
from rules.anomaly import detect_anomalies
import pandas as pd

def analyze_dataset(df: pd.DataFrame):
    return {
        "empty_cells": detect_empty_cells(df),
        "empty_columns": detect_empty_columns(df),
        "duplicates": detect_duplicates(df),
        "date_cols": detect_date_columns(df),
        "currency_cols": detect_currency_columns(df),
        "typos": detect_typos_fuzzy(df),
        "anomalies": detect_anomalies(df)
    }
