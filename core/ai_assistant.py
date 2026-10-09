import pandas as pd
from core.analyzer import analyze_dataset
from rules.empty import fill_empty_cells, drop_empty_columns
from rules.duplicate import remove_duplicates
from rules.formatting import trim_whitespace
from rules.datatype import normalize_dates, normalize_currency, detect_date_columns, detect_currency_columns
from rules.anomaly import cap_anomalies, detect_anomalies

class LocalAIAssistant:
    def __init__(self):
        pass

    def generate_plan(self, df: pd.DataFrame) -> list:
        analysis = analyze_dataset(df)
        plan = []
        
        if analysis["empty_cells"] > 0:
            plan.append({
                "step": "Fill Missing Cells",
                "description": f"Found {analysis['empty_cells']} empty cells. Fill numeric with 0 and text with 'Unknown'."
            })
            
        if analysis["empty_columns"]:
            plan.append({
                "step": "Drop Empty Columns",
                "description": f"Found completely empty columns: {analysis['empty_columns']}. Remove them."
            })
            
        if analysis["duplicates"] > 0:
            plan.append({
                "step": "Remove Duplicates",
                "description": f"Found {analysis['duplicates']} duplicate rows. Drop duplicates."
            })
            
        plan.append({
            "step": "Trim Whitespace",
            "description": "Clean leading and trailing spaces from all text columns."
        })
        
        if analysis["date_cols"]:
            plan.append({
                "step": "Normalize Dates",
                "description": f"Normalize date formats in columns: {analysis['date_cols']}."
            })
            
        if analysis["currency_cols"]:
            plan.append({
                "step": "Normalize Currency/Numbers",
                "description": f"Clean and convert currency/number format in columns: {analysis['currency_cols']}."
            })
            
        if analysis["anomalies"]:
            cols_with_outliers = list(analysis["anomalies"].keys())
            plan.append({
                "step": "Cap Outliers (Anomalies)",
                "description": f"Cap statistical outliers using IQR in columns: {cols_with_outliers}."
            })
            
        return plan

    def execute_instruction(self, df: pd.DataFrame, instruction: str) -> tuple[pd.DataFrame, str]:
        instruction_lower = instruction.lower()
        df_clean = df.copy()
        msg = ""
        
        if "duplikat" in instruction_lower or "duplicate" in instruction_lower:
            count = df_clean.duplicated().sum()
            df_clean = remove_duplicates(df_clean)
            msg = f"Successfully removed {count} duplicate rows."
            
        elif "kosong" in instruction_lower or "empty" in instruction_lower or "missing" in instruction_lower:
            count = df_clean.isnull().sum().sum()
            df_clean = fill_empty_cells(df_clean)
            msg = f"Successfully filled {count} empty cells."
            
        elif "spasi" in instruction_lower or "whitespace" in instruction_lower or "trim" in instruction_lower:
            df_clean = trim_whitespace(df_clean)
            msg = "Successfully trimmed whitespaces from text columns."
            
        elif "tanggal" in instruction_lower or "date" in instruction_lower:
            date_cols = detect_date_columns(df_clean)
            if date_cols:
                df_clean = normalize_dates(df_clean, date_cols)
                msg = f"Successfully normalized dates in columns: {date_cols}."
            else:
                msg = "No date columns detected."
                
        elif "mata uang" in instruction_lower or "currency" in instruction_lower or "angka" in instruction_lower:
            curr_cols = detect_currency_columns(df_clean)
            if curr_cols:
                df_clean = normalize_currency(df_clean, curr_cols)
                msg = f"Successfully normalized currency in columns: {curr_cols}."
            else:
                msg = "No currency columns detected."
                
        elif "outlier" in instruction_lower or "anomaly" in instruction_lower or "anomali" in instruction_lower:
            anomalies = detect_anomalies(df_clean)
            for col, info in anomalies.items():
                df_clean = cap_anomalies(df_clean, col, info['lower_bound'], info['upper_bound'])
            msg = f"Successfully capped anomalies in columns: {list(anomalies.keys())}."
            
        elif "semua" in instruction_lower or "all" in instruction_lower or "automasi" in instruction_lower:
            df_clean = fill_empty_cells(df_clean)
            df_clean = remove_duplicates(df_clean)
            df_clean = trim_whitespace(df_clean)
            d_cols = detect_date_columns(df_clean)
            if d_cols:
                df_clean = normalize_dates(df_clean, d_cols)
            c_cols = detect_currency_columns(df_clean)
            if c_cols:
                df_clean = normalize_currency(df_clean, c_cols)
            msg = "Executed comprehensive local AI cleaning pipeline successfully."
            
        else:
            msg = "Instruction not recognized. Try keywords like 'duplikat', 'kosong', 'spasi', 'tanggal', 'outlier', or 'semua'."
            
        return df_clean, msg
