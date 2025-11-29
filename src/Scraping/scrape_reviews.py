import csv
import time
from datetime import datetime
from google_play_scraper import reviews, Sort
from tqdm import tqdm
import os

# --- Configuration ---

# Target number of reviews to collect per bank application
TARGET_PER_BANK = 400
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# IDs -> Bank names based on provided URLs
APPS = {
    "com.combanketh.mobilebanking": "Commercial Bank of Ethiopia (CBE)",
    "com.boa.boaMobileBanking": "Bank of Abyssinia (BOA)",
    "com.dashen.dashensuperapp": "Dashen Bank"
}

# --- Utility Functions ---

def iso_date(d):
    """Converts a datetime object to an ISO date string."""
    return d.date().isoformat() if d else None

def scrape_one(package_name, bank_name, target=TARGET_PER_BANK):
    """
    Scrapes Google Play reviews for a single application package.

    Args:
        package_name (str): The package ID of the app (e.g., 'com.app.name').
        bank_name (str): The friendly name of the bank for logging/data.
        target (int): The maximum number of reviews to collect.

    Returns:
        list: A list of dictionaries, where each dictionary is a review record.
    """
    collected = []
    count = 0
    continuation_token = None
    # Initialize the progress bar for visual tracking
    pbar = tqdm(total=target, desc=f"Scraping {bank_name}")
    
    while count < target:
        try:
            # Fetch a batch of reviews (up to 200 per call)
            result, continuation_token = reviews(
                package_name,
                sort=Sort.NEWEST,      # Sort by newest first
                count=200,             # Number of reviews to fetch per batch
                continuation_token=continuation_token  # Continue from last batch
)
        except Exception as e:
            print(f"\n[ERROR] An error occurred while scraping {bank_name}: {e}")
            break # Exit the loop on error

        if not result:
            break # No more reviews available

        for r in result:
            collected.append({
                "review_id": r.get("reviewId"),
                "review": r.get("content") or "",
                "rating": r.get("score"),
                "date": iso_date(r.get("at")),
                "bank": bank_name,
                "app_package": package_name,
                "source": "google_play"
            })
            count += 1
            pbar.update(1)
            if count >= target:
                break
        
        # Wait a second between requests to avoid potential rate limiting
        time.sleep(1)
        
        if continuation_token is None:
            break # All pages have been scraped
            
    pbar.close()
    return collected

def save_csv(rows, filename):
    """Saves a list of dictionaries to a CSV file."""
    keys = ["review_id","review","rating","date","bank","app_package","source"]
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        print(f"Successfully saved {len(rows)} rows to {filename}")
    except Exception as e:
        print(f"[ERROR] Could not save file {filename}: {e}")

# --- Main Logic ---

def main(target=TARGET_PER_BANK):
    """
    Main function to orchestrate the scraping process for all defined apps.
    """
    all_rows = []
    print(f"Starting review scraping for {len(APPS)} applications (Target: {target} reviews per app).")
    
    for pkg, bank in APPS.items():
        print(f"\n--- Processing: {bank} ({pkg}) ---")
        rows = scrape_one(pkg, bank, target)
        
        # Save individual bank data
        filename = os.path.join(OUTPUT_DIR, f"{pkg.replace('.','_')}_raw.csv")
        save_csv(rows, filename)
        
        all_rows.extend(rows)
        
    # Save combined data
    combined_path = os.path.join(OUTPUT_DIR, "combined_raw.csv")
    save_csv(all_rows, combined_path)
    
    print(f"\n--- COMPLETE ---")
    print(f"Total rows collected across all apps: {len(all_rows)}")
    print(f"Saved combined CSV: {combined_path}")

if __name__ == "__main__":
    main()