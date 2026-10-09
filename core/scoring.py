import pandas as pd

def calculate_confidence_score(df: pd.DataFrame) -> int:
    if df is None or len(df) == 0:
        return 0
    total_cells = df.shape[0] * df.shape[1]
    if total_cells == 0:
        return 100
    
    missing_cells = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    
    missing_penalty = (missing_cells / total_cells) * 60
    duplicate_penalty = (duplicates / len(df)) * 40 if len(df) > 0 else 0
    
    score = max(0, min(100, int(100 - missing_penalty - duplicate_penalty)))
    return score
