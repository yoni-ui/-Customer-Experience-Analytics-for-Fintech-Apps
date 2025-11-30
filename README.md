Customer Experience Analytics for Ethiopian Fintech Apps
Submission Report
Prepared By: Yonas Yishak

Project: Bank Review Analytics - Tasks 1 to 4

This report details the successful execution of the first four tasks of the "Bank Review Analytics" project, which established a robust data pipeline and initial analytical insights for three major Ethiopian fintech applications: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

🎯 Project Objective
The primary goal is to scrape, preprocess, analyze, and store user reviews from the Google Play Store for the selected applications. The analysis aims to extract actionable insights regarding app performance, user satisfaction, and feature prioritization to guide product improvement strategies for the respective banks.

🛠️ Methodology & Results by Task
Task 1 — Data Collection & Preprocessing
Goal: Collect raw review data and transform it into a clean, ready-for-analysis dataset.

Methodology: The google-play-scraper Python library was used to collect ≥400 reviews (text, rating, date, bank name) for each bank's package ID (cbe.mobile, com.bankofabyssinia.app, com.dashenbank.app).

Preprocessing Steps: Merging raw files, removing duplicates, handling missing data, coercing ratings, and normalizing dates.

Output File	Description	Row Count
data/raw/combined_raw.csv	Initial merged, uncleaned data.	1,200+
data/processed/clean_reviews.csv	Final dataset, ready for analysis.	Verified

Export to Sheets

Task 2 — Sentiment & Theme Analysis
Goal: Classify the cleaned reviews by sentiment and group them into primary themes to quantify user opinions.

Sentiment Analysis: The VADER transformer model was used to classify reviews into POSITIVE, NEUTRAL, or NEGATIVE sentiment labels.

Thematic Analysis: TF-IDF and spaCy were employed to extract keywords and group critical feedback into five primary themes: Account Access, Transaction Performance, User Interface, App Stability, and Customer Support.

Bank	NEGATIVE	NEUTRAL	POSITIVE
BOA	76	124	134
CBE	31	133	162
Dashen Bank	52	83	175

Export to Sheets

Task 3 — PostgreSQL Storage
Goal: Establish a persistent, queryable database to store the processed review data.

Methodology: A bank_reviews PostgreSQL database was created.

Schema: Two tables were defined: Banks (bank_id, bank_name) and Reviews (containing review details, rating, sentiment, theme, linked via FK to bank_id).

Tools: PostgreSQL, Python with psycopg2 and SQLAlchemy.

Result: The database is populated with all ≈1,200 cleaned, classified reviews, enabling efficient data retrieval for future dashboarding and analytics.

Task 4 — Insights & Visualization
Goal: Extract meaningful insights from the combined dataset and visualize the key findings.

Data: Used ≈970 reviews with merged sentiment and theme columns (data/processed/clean_reviews_with_sentiment_and_themes.csv).

📊 Key Results
Metric	Bank of Abyssinia (BOA)	Commercial Bank of Ethiopia (CBE)	Dashen Bank
Average Rating	3.12	3.98	3.75

Export to Sheets

Insight: CBE has the highest overall average customer rating.

Shutterstock
Explore

Critical Theme	BOA	CBE	Dashen Bank
Account Access	12	15	12
Transaction Performance	25	12	20

Export to Sheets

Insight: Transaction Performance and Account Access are consistently recurring critical issues across all banks.

🖼️ Visualizations
The following plots are generated and stored in the plots/ directory:

plots/average_rating_per_bank.png

plots/sentiment_counts_per_bank.png

plots/theme_counts_per_bank.png

💡 Overall Conclusion & Recommendations
The completed tasks provide a strong analytical foundation for understanding customer experience.

Top Performers: CBE and Dashen Bank exhibit higher customer satisfaction based on superior average ratings and higher positive sentiment counts.

Key Pain Points: The most significant areas for mandatory improvement across all three applications are Account Access and Transaction Performance. These themes are directly linked to core banking app functionality and are major sources of user frustration.

Actionability: The structured insights and visualizations, now backed by a persistent PostgreSQL database, offer actionable data to guide product teams toward specific feature improvements, customer support enhancements, and stability fixes.

📂 Appendix (File Structure)
.
├── data/
│   ├── raw/
│   │   └── combined_raw.csv        # Raw, merged data
│   └── processed/
│       ├── clean_reviews.csv       # Cleaned data (after Task 1)
│       └── clean_reviews_with_sentiment_and_themes.csv # Final merged dataset (for Task 4)
├── plots/
│   ├── average_rating_per_bank.png
│   ├── sentiment_counts_per_bank.png
│   └── theme_counts_per_bank.png
└── src/
    ├── scraping/                   # Task 1: Data collection scripts
    ├── preprocessing/              # Task 1: Data cleaning scripts
    ├── task_2/                     # Task 2: Sentiment and theme analysis scripts
    ├── task_3/                     # Task 3: PostgreSQL storage scripts
    └── task_4/
        ├── visualizations/         # Task 4: Plotting scripts (e.g., insights_plot.py)
        └── insights.py             # Task 4: Insight calculation script
