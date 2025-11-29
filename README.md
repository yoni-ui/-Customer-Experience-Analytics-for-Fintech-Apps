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

Task 2 — Sentiment & Theme Analysis
- Applied VADER transformer for sentiment scoring (90%+ coverage).
- Extracted themes using keyword extraction + clustering.
- Produced:
  - sentiment_results.csv
  - themes_summary.json
- Code organized in /analysis and /utils folders.
bank                               theme
Bank of Abyssinia (BOA)            Account Access              12
                                   App Stability               10
                                   Customer Support             6
                                   Other                      276
                                   Transaction Performance     25
                                   User Interface               5
Commercial Bank of Ethiopia (CBE)  Account Access              15
                                   App Stability                2
                                   Customer Support             7
                                   Other                      289
                                   Transaction Performance     12
                                   User Interface               1
Dashen Bank                        Account Access              12
                                   App Stability                7
                                   Customer Support             5
                                   Other                      249
                                   Transaction Performance     20
                                   User Interface              17
dtype: int64
bank                               sentiment_label
Bank of Abyssinia (BOA)            NEGATIVE            76
                                   NEUTRAL            124
                                   POSITIVE           134
Commercial Bank of Ethiopia (CBE)  NEGATIVE            31
                                   NEUTRAL            133
                                   POSITIVE           162
Dashen Bank                        NEGATIVE            52
                                   NEUTRAL             83
                                   POSITIVE           175
