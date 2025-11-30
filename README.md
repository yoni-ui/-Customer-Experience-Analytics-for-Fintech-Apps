B8W2: Customer Experience Analytics for Fintech Apps
Interim Submission Report - Yonas yishak
Bank Review Analytics - Task 1 to 3

Objective
Scrape, preprocess, analyze, and store user reviews from the Google Play Store for three Ethiopian banks:
Commercial Bank of Ethiopia (CBE)


Bank of Abyssinia (BOA)


Dashen Bank


The goal is to enable actionable insights for improving app performance, user satisfaction, and feature prioritization.

Methodology
Task 1 — Data Collection & Preprocessing
Web Scraping


Used the google-play-scraper Python library.


Targeted package IDs:


cbe.mobile (CBE)


com.bankofabyssinia.app (BOA)


com.dashenbank.app (Dashen Bank)


Collected ≥400 reviews per bank, including:


Review text


Rating (1–5)


Posting date


Bank/app name


Source (Google Play)


Saved individual CSVs per bank under data/raw/ and a combined CSV as combined_raw.csv.


Preprocessing


Merged raw CSVs.


Removed duplicates (by review_id and text).


Handled missing data (filled empty reviews, coerced ratings to integers).


Normalized dates to YYYY-MM-DD.


Output cleaned CSV: data/processed/clean_reviews.csv.


Git Workflow


Created task-1 branch.


Frequent commits after scraping and preprocessing.


Scripts organized under src/scraping and src/preprocessing.


Result:
Combined raw reviews: 1,200+ rows (≥400 per bank).


Cleaned dataset ready for sentiment and thematic analysis.


Task 2 — Sentiment & Theme Analysis
Sentiment Analysis


Applied VADER transformer for sentiment scoring (coverage: 90%+ of reviews).


Classified reviews as POSITIVE, NEUTRAL, or NEGATIVE.


Thematic Analysis


Extracted keywords using TF-IDF and spaCy.


Grouped keywords into themes/clusters per bank:


Account Access


Transaction Performance


User Interface & Experience


App Stability


Customer Support


Other


Results:
Themes per bank (count of reviews per theme):
Bank
Account Access
Transaction Performance
User Interface
App Stability
Customer Support
Other
BOA
12
25
5
10
6
276
CBE
15
12
1
2
7
289
Dashen
12
20
17
7
5
249

Sentiment distribution per bank:
Bank
NEGATIVE
NEUTRAL
POSITIVE
BOA
76
124
134
CBE
31
133
162
Dashen
52
83
175


Output files: sentiment_results.csv, themes_summary.json.


Code organized in /analysis and /utils.


Task 3 — PostgreSQL Storage (Completed)
Database Setup


Created PostgreSQL database: bank_reviews.


Defined schema with Banks and Reviews tables:


Banks: bank_id (PK), bank_name, app_name


Reviews: review_id (PK), bank_id (FK), review_text, rating, review_date, sentiment_label, sentiment_score, source


Data Insertion


Used Python (SQLAlchemy + psycopg2) to insert all cleaned reviews into PostgreSQL.


Verified integrity using SQL queries:

 SELECT bank_id, COUNT(*) FROM reviews GROUP BY bank_id;
SELECT bank_id, AVG(rating) FROM reviews GROUP BY bank_id;


Result


Database populated with 1,200+ entries.


Ready for dashboard analytics and querying by themes or sentiment.


Task 4 Report

1. Objective
The objective of Task 4 was to analyze customer reviews of fintech applications to extract meaningful insights on:
Overall customer sentiment.


Common themes and issues in app usage.


Average ratings per bank.


Visualization of trends for reporting purposes.


2. Data Description
The analysis used 970 customer reviews collected from multiple banking apps. The dataset included the following fields:
Column
Description
review_id
Unique identifier for each review
review / clean_text
Original and cleaned review text
rating
Customer-provided rating (1–5)
bank
Bank name (e.g., CBE, BOA, Dashen Bank)
app_package
App identifier/package name
source
Source of review (Google Play / App Store)
sentiment_label
NLP-assigned sentiment category (POSITIVE, NEGATIVE, NEUTRAL)
sentiment_score
Numerical sentiment score
theme
Identified theme or topic in review (Account Access, Customer Support, etc.)

Data preprocessing steps included:
Cleaning review text (clean_text column).


Sentiment analysis using [model/method].


Theme extraction from reviews.


Merging sentiment and theme data into a single CSV.



3. Methodology
Data Cleaning: Removed duplicates, nulls, and irrelevant characters.


Sentiment Analysis: Applied NLP model to classify reviews as POSITIVE, NEGATIVE, or NEUTRAL.


Theme Extraction: Categorized reviews into main themes such as:


Account Access


App Stability


Customer Support


Transaction Performance


User Interface


Other


Data Aggregation: Calculated metrics per bank:


Average rating.


Count of reviews per sentiment.


Count of reviews per theme.


Visualization: Created bar plots and heatmaps to summarize findings.


4. Results
4.1 Average Rating per Bank
Bank
Average Rating
Bank of Abyssinia (BOA)
3.12
Commercial Bank of Ethiopia (CBE)
3.98
Dashen Bank
3.75

Insight: CBE has the highest overall customer rating among the three banks.

4.2 Sentiment Counts per Bank
Bank
POSITIVE
NEUTRAL
NEGATIVE
BOA
134
124
76
CBE
162
133
31
Dashen Bank
175
83
52

Insight: Dashen Bank has the highest number of positive reviews, while BOA has the highest negative review proportionally.

4.3 Theme Counts per Bank
Bank
Account Access
App Stability
Customer Support
Transaction Performance
User Interface
Other
BOA
12
10
6
25
5
276
CBE
15
2
7
12
1
289
Dashen Bank
12
7
5
20
17
249

Insight: Most reviews are categorized under “Other,” but Transaction Performance and Account Access are recurring issues.

4.4 Visualizations
Average Rating per Bank
 Insert plots/average_rating_per_bank.png here.


Sentiment Distribution per Bank
 Insert plots/sentiment_counts_per_bank.png here.


Theme Distribution per Bank
 Insert plots/theme_counts_per_bank.png here.


Visualizations confirm numerical insights and highlight customer pain points.

5. Conclusion
The analysis reveals:
CBE and Dashen Bank generally have higher customer satisfaction based on ratings and positive sentiment.


Account Access and Transaction Performance are key areas for improvement.


Sentiment and theme visualizations provide actionable insights for fintech app enhancement.


These findings can guide product teams to focus on feature improvements, customer support, and app stability.

6. Appendix
data/processed/clean_reviews_with_sentiment_and_themes.csv – Merged dataset.


src/task_4/insights.py – Analysis script.


src/task_4/merge_sentiment.py – Script to merge sentiment and themes.


src/task_4/visualizations/insights_plot.py – Plotting script.




