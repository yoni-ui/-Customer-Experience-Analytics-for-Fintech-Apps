import pandas as pd
import os

RAW_DIR = "data/raw"

# List of expected CSVs
bank_files = {
    "CBE": "cbe_mobile_raw.csv",
    "BOA": "com_bankofabyssinia_app_raw.csv",
    "Dashen": "com_dashenbank_app_raw.csv"
}

for bank, file_name in bank_files.items():
    file_path = os.path.join(RAW_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        total = len(df)
        print(f"{bank}: {total} reviews")
        if total >= 400:
            print(f"✅ {bank} has sufficient reviews (≥400)")
        else:
            print(f"⚠️ {bank} has less than 400 reviews! Consider fetching more.\n")
    else:
        print(f"❌ {file_name} not found!\n")
