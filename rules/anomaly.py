import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame):
    anomalies = {}
    for col in df.select_dtypes(include=[np.number]):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if len(outliers) > 0:
            anomalies[col] = {
                'count': len(outliers),
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
    return anomalies

def cap_anomalies(df: pd.DataFrame, column: str, lower: float, upper: float) -> pd.DataFrame:
    df_clean = df.copy()
    df_clean[column] = np.clip(df_clean[column], lower, upper)
    return df_clean

def get_anomaly_rows(df: pd.DataFrame, column: str, lower: float, upper: float) -> pd.DataFrame:
    return df[(df[column] < lower) | (df[column] > upper)]
