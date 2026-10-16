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
    
    distinct_keywords = {
        "utara", "selatan", "timur", "barat", "pusat", "central", "north", "south", "east", "west",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "i", "ii", "iii", "iv", "v",
        "a", "b", "c", "d", "e", "f", "g", "h",
        "aktif", "nonaktif", "active", "inactive", "enabled", "disabled",
        "true", "false", "yes", "no", "baru", "lama", "new", "old",
        "laki-laki", "perempuan", "pria", "wanita", "male", "female"
    }
    
    if len(words1) == len(words2) and len(words1) > 0:
        diff_count = 0
        diff_w1, diff_w2 = "", ""
        for w1, w2 in zip(words1, words2):
            if w1 != w2:
                diff_count += 1
                diff_w1, diff_w2 = w1, w2
        if diff_count == 1:
            if diff_w1 in distinct_keywords and diff_w2 in distinct_keywords:
                return True
                
        # Also consider different numbers/letters as distinct if they are the only difference
        if diff_w1.isdigit() and diff_w2.isdigit():
            return True
        if len(diff_w1) == 1 and len(diff_w2) == 1 and diff_w1.isalnum() and diff_w2.isalnum():
            return True
            
        # Additional heuristic: If the differing word is a common generic word, don't flag as typo
        if (len(diff_w1) < 4 or len(diff_w2) < 4) and (sim := similar(diff_w1, diff_w2)) < 0.6:
            return True
                
    if len(words1) > 1 and len(words2) > 1 and words1[:-1] == words2[:-1]:
        last1, last2 = words1[-1], words2[-1]
        if last1 in distinct_keywords and last2 in distinct_keywords:
            return True
                
    return False

def detect_typos_fuzzy(df: pd.DataFrame, threshold=0.92):
    typo_suggestions = {}
    exclude_keywords = [
        'id', 'code', 'telp', 'phone', 'postal', 'zip', 'tahun', 'year', 'nik', 'npwp', 
        'number', 'no', 'date', 'email', 'url', 'password', 'token', 'uuid', 'guid', 
        'nomor', 'kode', 'alamat', 'address', 'deskripsi', 'description', 'keterangan', 
        'notes', 'catatan', 'nama', 'name', 'tanggal', 'waktu', 'time', 'status', 'gender', 'jenis'
    ]
    
    for col in df.select_dtypes(include=['object', 'string']):
        col_lower = col.lower()
        if "id" in col_lower or "code" in col_lower or "nik" in col_lower or "nomor" in col_lower or "kode" in col_lower or "no " in col_lower or "no." in col_lower:
            continue
        if any(kw in col_lower for kw in exclude_keywords) or (len(col_lower) <= 3 and col_lower == 'id') or col_lower == 'no':
            continue
            
        try:
            if len(df) > 5 and df[col].nunique() / len(df) > 0.4:
                continue
            
            avg_len = df[col].dropna().astype(str).str.len().mean()
            if avg_len > 20:
                continue
        except Exception:
            pass
            
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
                
                # Exclude purely alphanumeric IDs or codes that are not words
                if (any(c.isdigit() for c in v1) and any(c.isdigit() for c in v2)) and \
                    (not " " in v1  and not " " in v2) and (len(v1) < 10 and len(v2) < 10):
                    continue
                    
                # Exclude extremely short words where 1 char diff is completely different meaning
                if len(v1) <= 4 and len(v2) <= 4:
                    continue
                    
                if is_distinct_category_variant(v1, v2):
                    continue
                    
                if abs(len(v1) - len(v2)) > 3:
                    continue
                    
                sim = similar(v1, v2)
                
                # Dynamic threshold: longer words need lower similarity ratio to catch typos
                dynamic_threshold = threshold
                max_len = max(len(v1), len(v2))
                if max_len > 12:
                    dynamic_threshold = max(0.80, threshold - 0.06)
                elif max_len <= 5:
                    dynamic_threshold = min(0.92, threshold + 0.04)

                if sim >= dynamic_threshold and sim < 1.0:
                    count_v1 = int(value_counts.get(unique_vals[i], 1))
                    count_v2 = int(value_counts.get(unique_vals[j], 1))
                    
                    if count_v1 >= 3 * count_v2 or count_v2 <= 3:
                        # Additional check to ensure high confidence:
                        # Don't suggest fix if counts are similar and relatively high
                        if count_v1 > 1 and count_v2 > 1 and count_v1 < 3 * count_v2 and count_v2 < 3 * count_v1:
                            continue
                        
                        if count_v1 >= count_v2:
                            pair_key = tuple(sorted([v1, v2]))
                            if pair_key not in seen:
                                seen.add(pair_key)
                                # v1 is more frequent or equal, so suggest v1 (v1, v2)
                                pairs.append((v1, v2))
                        else:
                            pair_key = tuple(sorted([v1, v2]))
                            if pair_key not in seen:
                                seen.add(pair_key)
                                # v2 is more frequent, so suggest v2 (v2, v1)
                                pairs.append((v2, v1))
                            
        if pairs:
            typo_suggestions[col] = pairs
            
    return typo_suggestions

def fix_typo(df: pd.DataFrame, column: str, target: str, replacement: str) -> pd.DataFrame:
    df_clean = df.copy()
    # Use standard string replace for complete accuracy
    df_clean[column] = df_clean[column].apply(lambda x: replacement if str(x) == target else x)
    return df_clean

def get_typo_rows(df: pd.DataFrame, column: str, target: str) -> pd.DataFrame:
    return df[df[column].astype(str) == target]
