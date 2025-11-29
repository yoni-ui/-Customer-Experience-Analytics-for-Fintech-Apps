#!/usr/bin/env python3
# database/scripts/insert_data.py
"""
Insert cleaned review data into PostgreSQL.

Usage:
  pip install -r requirements.txt
  export DB_NAME=bank_reviews DB_USER=postgres DB_PASS=postgrespw DB_HOST=localhost DB_PORT=5432 CSV_PATH=data/processed/reviews_with_themes.csv
  python database/scripts/insert_data.py
"""

import os
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from datetime import datetime

# Load env
DB_NAME = os.getenv("DB_NAME", "bank_reviews")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgrespw")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
CSV_PATH = os.getenv("CSV_PATH", "data/processed/reviews_with_themes.csv")

BATCH_SIZE = 500  # insert in batches

def connect():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def ensure_banks(cur, df):
    """Insert unique banks into banks table (idempotent via ON CONFLICT)."""
    banks = df['bank'].dropna().unique().tolist()
    sql = """
        INSERT INTO banks (bank_name, app_name)
        VALUES %s
        ON CONFLICT (bank_name) DO NOTHING
        RETURNING bank_id, bank_name;
    """
    values = [(b, b + " App") for b in banks]
    execute_values(cur, sql, values)

def get_bank_id_map(cur):
    cur.execute("SELECT bank_id, bank_name FROM banks;")
    rows = cur.fetchall()
    return {r[1]: r[0] for r in rows}

def prepare_review_row(row, bank_id):
    # row is a pandas Series
    external_id = row.get('review_id') if 'review_id' in row else None
    text = row.get('review') or ""
    rating = int(row['rating']) if pd.notna(row.get('rating')) else None
    date = None
    if pd.notna(row.get('date')):
        try:
            date = pd.to_datetime(row['date']).date()
        except Exception:
            date = None
    sentiment_label = row.get('sentiment_label')
    sentiment_score = None
    if pd.notna(row.get('sentiment_score')):
        try:
            sentiment_score = float(row['sentiment_score'])
        except Exception:
            sentiment_score = None
    theme = row.get('theme') if 'theme' in row else None
    source = row.get('source') if 'source' in row else 'google_play'
    return (
        external_id, bank_id, text, rating, date, sentiment_label, sentiment_score, theme, source
    )

def insert_reviews(conn, cur, df):
    bank_map = get_bank_id_map(cur)
    rows_to_insert = []
    for _, row in df.iterrows():
        bank_name = row.get('bank')
        bank_id = bank_map.get(bank_name)
        if not bank_id:
            # Should not happen; skip if bank not found
            continue
        rows_to_insert.append(prepare_review_row(row, bank_id))
        if len(rows_to_insert) >= BATCH_SIZE:
            _batch_insert(cur, rows_to_insert)
            conn.commit()
            rows_to_insert = []
    if rows_to_insert:
        _batch_insert(cur, rows_to_insert)
        conn.commit()

def _batch_insert(cur, rows):
    sql = """
    INSERT INTO reviews
    (external_review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, theme, source)
    VALUES %s
    ON CONFLICT DO NOTHING;
    """
    execute_values(cur, sql, rows, page_size=100)

def main():
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"CSV file not found: {CSV_PATH}")
    print("Loading CSV:", CSV_PATH)
    df = pd.read_csv(CSV_PATH)
    print("Rows in CSV:", len(df))

    conn = connect()
    cur = conn.cursor()
    try:
        print("Ensuring banks present in 'banks' table...")
        ensure_banks(cur, df)
        conn.commit()
        print("Inserting reviews (batch size:", BATCH_SIZE, ") ...")
        insert_reviews(conn, cur, df)
        print("Done inserting.")
    except Exception as e:
        conn.rollback()
        print("Error occurred:", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
