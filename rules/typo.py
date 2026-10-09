import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def is_distinct_category_variant(v1: str, v2: str) -> bool:
    s1, s2 = v1.strip().lower(), v2.strip().lower()
    if s1 == s2:
        return False
    
    words1 = s1.split()
    words2 = s2.split()
    
    distinct_sets = [
        {"utara", "selatan", "timur", "barat", "pusat", "central", "north", "south", "east", "west"},
        {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "i", "ii", "iii", "iv", "v"},
        {"a", "b", "c", "d", "e", "f", "g", "h"},
        {"aktif", "nonaktif", "active", "inactive", "enabled", "disabled"},
        {"true", "false", "yes", "no"}
    ]
    
    if len(words1) == len(words2) and len(words1) > 0:
        diff_count = 0
        diff_w1, diff_w2 = "", ""
        for w1, w2 in zip(words1, words2):
            if w1 != w2:
                diff_count += 1
                diff_w1, diff_w2 = w1, w2
        if diff_count == 1:
            for dset in distinct_sets:
                if diff_w1 in dset and diff_w2 in dset:
                    return True
                    
    if len(words1) > 1 and len(words2) > 1 and words1[:-1] == words2[:-1]:
        last1, last2 = words1[-1], words2[-1]
        for dset in distinct_sets:
            if last1 in dset and last2 in dset:
                return True
                
    return False

def detect_typos_fuzzy(df: pd.DataFrame, threshold=0.80):
    typo_suggestions = {}
    exclude_keywords = ['id', 'code', 'telp', 'phone', 'postal', 'zip', 'tahun', 'year', 'nik', 'npwp', 'number', 'no', 'date', 'email', 'url']
    
    for col in df.select_dtypes(include=['object', 'string']):
        col_lower = col.lower()
        if any(kw in col_lower for kw in exclude_keywords):
            continue
            
        value_counts = df[col].value_counts()
        unique_vals = value_counts.index.tolist()
        
        if not (1 < len(unique_vals) < max(200, len(df) * 0.4)):
            continue
            
        seen = set()
        pairs = []
        for i in range(len(unique_vals)):
            for j in range(i+1, len(unique_vals)):
                v1 = str(unique_vals[i]).strip()
                v2 = str(unique_vals[j]).strip()
                
                if v1.isdigit() or v2.isdigit() or len(v1) < 3 or len(v2) < 3:
                    continue
                    
                if is_distinct_category_variant(v1, v2):
                    continue
                    
                if abs(len(v1) - len(v2)) > 3:
                    continue
                    
                sim = similar(v1, v2)
                if threshold <= sim < 1.0:
                    count_v1 = int(value_counts.get(unique_vals[i], 1))
                    count_v2 = int(value_counts.get(unique_vals[j], 1))
                    
                    if count_v1 >= 3 * count_v2 or count_v2 <= 3:
                        pair_key = tuple(sorted([v1, v2]))
                        if pair_key not in seen:
                            seen.add(pair_key)
                            # v1 is more frequent (index i < j), so pair is (v1, v2)
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
