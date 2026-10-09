import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def detect_typos_fuzzy(df: pd.DataFrame, threshold=0.85):
    typo_suggestions = {}
    for col in df.select_dtypes(include=['object', 'string']):
        unique_vals = df[col].dropna().unique()
        if 1 < len(unique_vals) < max(50, len(df) * 0.2):
            for i in range(len(unique_vals)):
                for j in range(i+1, len(unique_vals)):
                    v1, v2 = str(unique_vals[i]), str(unique_vals[j])
                    if 0.7 < similar(v1, v2) < 1.0:
                        if col not in typo_suggestions:
                            typo_suggestions[col] = []
                        typo_suggestions[col].append((v1, v2))
    return typo_suggestions

def fix_typo(df: pd.DataFrame, column: str, target: str, replacement: str) -> pd.DataFrame:
    df_clean = df.copy()
    df_clean[column] = df_clean[column].replace(target, replacement)
    return df_clean

def get_typo_rows(df: pd.DataFrame, column: str, target: str) -> pd.DataFrame:
    return df[df[column] == target]
