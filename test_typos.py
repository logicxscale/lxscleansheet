import pandas as pd
from rules.typo import detect_typos_fuzzy

# Let's create a dummy dataframe with some common strings and see what gets detected
data = {
    'product': ['Laptop ASUS', 'Laptop ASUS', 'Laptop ASUS', 'Laptop ASCUS', 'Mouse Logitech', 'Mouse Logitehc', 'Mouse Logitech', 'Keyboard Mechanical', 'Keyboard Mechanical'],
    'city': ['Jakarta', 'Jakrta', 'Jakarta', 'Bandung', 'Bnadung', 'Surabaya', 'Surabayaa', 'Jakarta', 'Jakarta'],
    'category': ['Type A', 'Type B', 'Type A', 'Type C', 'Type D', 'Type E', 'Type A', 'Type A', 'Type B'],
    'status': ['Active', 'Inactive', 'Active', 'Aktif', 'Active', 'Inactiv', 'Inactive', 'Active', 'Active'],
    'name': ['John Doe', 'John doe', 'Jane Doe', 'Jon Doe', 'John Doe', 'John Die', 'Jane Doee', 'John Doe', 'John Doe'],
    'notes': ['Item condition is good', 'Item condition good', 'Item condition is excellent', 'Broken', 'Need repair', 'Needs repair', 'Fixed', 'New', 'Old'],
    'address': ['Jl. Sudirman No 10', 'Jl. Sudirman No 12', 'Jl Thamrin', 'Jl Sudirman No. 10', 'Jl. Gatot Subroto', 'Jl Gatot Subroto', 'Kuningan', 'Kuningan City', 'Sudirman']
}

df = pd.DataFrame(data)
typos = detect_typos_fuzzy(df)
import json
print(json.dumps(typos, indent=2))
