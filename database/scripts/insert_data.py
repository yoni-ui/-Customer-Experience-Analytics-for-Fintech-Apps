import psycopg2
import os
import csv
from dotenv import load_dotenv

# --- Load Environment Variables ---
# Determine the path to the .env file relative to this script.
# This fixes issues where the script is run from the root directory.
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

# --- Connection Details ---
# IMPORTANT: Hardcode 127.0.0.1 as a robust fallback for Windows/Docker routing issues.
DB_HOST_FALLBACK = "127.0.0.1"

DB_USER = os.getenv("DB_USER", "postgres")
# IMPORTANT: Ensure this password matches your POSTGRES_PASSWORD in docker-compose.yml
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword123") 
DB_NAME = os.getenv("DB_NAME", "bank_reviews")
DB_HOST = os.getenv("DB_HOST", DB_HOST_FALLBACK)
DB_PORT = os.getenv("DB_PORT", "5432")

# Assuming the data file path is correct relative to the root execution directory
RAW_DATA_PATH = "data/processed/combined_processed.csv" 

def connect():
    """Establishes a connection to the PostgreSQL database."""
    print("--- Connection Attempt Details ---")
    print(f"Loading .env file from: {env_path}")
    print(f"Host: {DB_HOST}, Port: {DB_PORT}, User: {DB_USER}, DB: {DB_NAME}")
    print(f"Password: {'*' * len(DB_PASSWORD)}") 
    print("----------------------------------")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"\n[FATAL ERROR] Connection failed.")
        print("1. Check if the 'bank_reviews_db' Docker container is running.")
        print(f"2. Check if the password '{DB_PASSWORD}' in .env matches the password in docker-compose.yml.")
        raise e

def insert_data(conn):
    """
    Reads data from the processed CSV and inserts it into the bank_reviews table.
    """
    if not os.path.exists(RAW_DATA_PATH):
        print(f"[ERROR] Data file not found at: {RAW_DATA_PATH}")
        print("Please ensure you have created the file 'data/processed/combined_processed.csv'.")
        return

    print(f"Loading data from: {RAW_DATA_PATH}")
    
    with open(RAW_DATA_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)  # Skip the header row
        except StopIteration:
            print("[ERROR] CSV file is empty. Skipping insertion.")
            return

        # Determine column indices dynamically
        # Added safety checks for column presence
        try:
            review_col = header.index("review")
            sentiment_col = header.index("sentiment")
        except ValueError:
            print("[ERROR] CSV header must contain 'review' and 'sentiment' columns. Skipping insertion.")
            return

        cur = conn.cursor()
        count = 0
        
        # Prepare the INSERT query
        insert_query = """
        INSERT INTO bank_reviews (review_text, sentiment)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """
        
        for row in reader:
            try:
                review_text = row[review_col]
                sentiment = row[sentiment_col]
                
                # PostgreSQL requires a table to exist, assuming schema.sql was run
                cur.execute(insert_query, (review_text, sentiment))
                count += 1
            except IndexError as e:
                print(f"[WARNING] Skipping malformed row: {row}")
            except Exception as e:
                # Catch any database-specific errors during insertion
                print(f"[DATABASE ERROR] Failed to insert row. Check schema definition: {e}")
                break # Stop processing on a critical error
                
        conn.commit()
        cur.close()
        print(f"Successfully inserted/updated {count} rows into bank_reviews.")


def main():
    conn = None
    try:
        # 1. Connect to the database
        conn = connect()
        
        # 2. Insert data
        insert_data(conn)
        
    except Exception as e:
        # The OperationalError is caught by connect() and re-raised
        # The connection error indicates we can't proceed.
        print(f"Insertion process aborted.")
        
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()