import pandas as pd

def validate_dataframe(df: pd.DataFrame) -> dict:
    results = {
        "has_data": len(df) > 0,
        "columns_count": len(df.columns),
        "row_count": len(df),
        "missing_values_total": int(df.isnull().sum().sum()),
        "duplicates_total": int(df.duplicated().sum())
    }
    return results
