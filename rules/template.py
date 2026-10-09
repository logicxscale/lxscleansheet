import pandas as pd

def check_schema_template(df: pd.DataFrame, template_cols: list) -> dict:
    actual_cols = list(df.columns)
    missing = [c for c in template_cols if c not in actual_cols]
    extra = [c for c in actual_cols if c not in template_cols]
    matched = [c for c in template_cols if c in actual_cols]
    
    return {
        "missing": missing,
        "extra": extra,
        "matched": matched,
        "match_percentage": (len(matched) / len(template_cols)) * 100 if template_cols else 100
    }
