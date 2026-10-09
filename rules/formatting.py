import pandas as pd

def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.select_dtypes(include=['object', 'string']):
        df_clean[col] = df_clean[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df_clean
