import pandas as pd
import os
from dateutil import parser

RAW_DIR = "data/raw"
OUT_DIR = "data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

def load_raw():
    files = [os.path.join(RAW_DIR,f) for f in os.listdir(RAW_DIR) if f.endswith(".csv")]
    dfs = [pd.read_csv(f, dtype=str) for f in files]
    return pd.concat(dfs, ignore_index=True)

def coerce_date(x):
    if pd.isnull(x):
        return pd.NA
    try:
        return pd.to_datetime(x).date().isoformat()
    except:
        try:
            return parser.parse(str(x)).date().isoformat()
        except:
            return pd.NA

def clean(df):
    df['review'] = df['review'].fillna('').str.strip()
    df = df[df['review'].str.len() > 0]
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0).astype(int)
    df['date'] = df['date'].apply(coerce_date)
    if df['review_id'].notna().sum() > 0:
        df = df.drop_duplicates(subset=['review_id'])
    df = df.drop_duplicates(subset=['review'])
    df['review'] = df['review'].str.replace(r'\s+', ' ', regex=True).str.strip()
    return df

def main():
    df = load_raw()
    cleaned = clean(df)
    out_path = os.path.join(OUT_DIR, "clean_reviews.csv")
    cleaned.to_csv(out_path, index=False, encoding='utf-8')
    print(f"Saved cleaned data: {out_path} (rows: {len(cleaned)})")

if __name__ == "__main__":
    main()
