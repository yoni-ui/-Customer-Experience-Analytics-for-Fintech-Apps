import csv
import time
from datetime import datetime
from google_play_scraper import reviews, Sort
from tqdm import tqdm
import os

TARGET_PER_BANK = 400
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Package IDs -> Bank names
APPS = {
    "cbe.mobile": "Commercial Bank of Ethiopia (CBE)",
    "com.bankofabyssinia.app": "Bank of Abyssinia (BOA)",
    "com.dashenbank.app": "Dashen Bank"
}

def iso_date(d):
    return d.date().isoformat() if d else None

def scrape_one(package_name, bank_name, target=TARGET_PER_BANK):
    collected = []
    count = 0
    continuation_token = None
    pbar = tqdm(total=target, desc=f"Scraping {bank_name}")
    while count < target:
        result, continuation_token = reviews(
            package_name,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=continuation_token
        )
        if not result:
            break
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
        time.sleep(1)
        if continuation_token is None:
            break
    pbar.close()
    return collected

def save_csv(rows, filename):
    keys = ["review_id","review","rating","date","bank","app_package","source"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def main(target=TARGET_PER_BANK):
    all_rows = []
    for pkg, bank in APPS.items():
        rows = scrape_one(pkg, bank, target)
        filename = os.path.join(OUTPUT_DIR, f"{pkg.replace('.','_')}_raw.csv")
        save_csv(rows, filename)
        all_rows.extend(rows)
    # combined
    combined_path = os.path.join(OUTPUT_DIR, "combined_raw.csv")
    save_csv(all_rows, combined_path)
    print(f"Saved combined CSV: {combined_path} (total rows: {len(all_rows)})")

if __name__ == "__main__":
    main()
