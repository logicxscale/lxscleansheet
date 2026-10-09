import pandas as pd
from rules.duplicate import detect_duplicates

def validate_dataframe(df: pd.DataFrame) -> dict:
    results = {
        "has_data": len(df) > 0,
        "columns_count": len(df.columns),
        "row_count": len(df),
        "missing_values_total": int(df.isnull().sum().sum()),
        "duplicates_total": detect_duplicates(df)
    }
    return results
