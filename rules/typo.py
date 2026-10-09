import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def detect_typos_fuzzy(df: pd.DataFrame, threshold=0.8):
    typo_suggestions = {}
    for col in df.select_dtypes(include=['object', 'string']):
        value_counts = df[col].value_counts()
        unique_vals = value_counts.index.tolist()
        if 1 < len(unique_vals) < max(100, len(df) * 0.3):
            seen = set()
            pairs = []
            for i in range(len(unique_vals)):
                for j in range(i+1, len(unique_vals)):
                    v1 = str(unique_vals[i])
                    v2 = str(unique_vals[j])
                    sim = similar(v1, v2)
                    if threshold <= sim < 1.0:
                        pair_key = tuple(sorted([v1, v2]))
                        if pair_key not in seen:
                            seen.add(pair_key)
                            pairs.append((v1, v2))
            if pairs:
                typo_suggestions[col] = pairs
    return typo_suggestions

def fix_typo(df: pd.DataFrame, column: str, target: str, replacement: str) -> pd.DataFrame:
    df_clean = df.copy()
    df_clean[column] = df_clean[column].replace(target, replacement)
    return df_clean

def get_typo_rows(df: pd.DataFrame, column: str, target: str) -> pd.DataFrame:
    return df[df[column] == target]
