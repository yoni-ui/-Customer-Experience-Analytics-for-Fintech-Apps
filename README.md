# Bank Review Analytics - Task 1

## Objective
Scrape and preprocess user reviews from Google Play Store for three Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Methodology

### 1. Web Scraping
- Used `google-play-scraper` Python library.
- Targeted the following package IDs:
  - `cbe.mobile` (CBE)
  - `com.bankofabyssinia.app` (BOA)
  - `com.dashenbank.app` (Dashen Bank)
- Fetched ≥400 reviews per bank, including:
  - Review text
  - Rating (1–5)
  - Posting date
  - Bank/app name
  - Source (`google_play`)
- Saved individual CSVs per bank in `data/raw` and combined CSV `combined_raw.csv`.

### 2. Preprocessing
- Merged all raw CSVs.
- Removed duplicates (by `review_id` and text).
- Handled missing data (filled empty reviews, coerced ratings to integers).
- Normalized dates to `YYYY-MM-DD`.
- Output cleaned CSV: `data/processed/clean_reviews.csv`.

### 3. Git Workflow
- Created `task-1` branch for all work.
- Frequent commits after scraping and preprocessing.
- Scripts organized under `src/scraping` and `src/preprocessing`.

## Results
- Combined raw reviews: 1,200+ rows (≥400 per bank)
- Cleaned dataset ready for sentiment and thematic analysis.
