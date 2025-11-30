Interim Submission Report: Customer Experience Analytics for Fintech Apps
Prepared By: Yonas Yishak Project: Bank Review Analytics - Tasks 1 to 4
1. Project Objective
The primary goal of this project is to scrape, preprocess, analyze, and store user reviews from the Google Play Store for three major Ethiopian fintech applications:
Commercial Bank of Ethiopia (CBE)
Bank of Abyssinia (BOA)
Dashen Bank
The analysis aims to extract actionable insights regarding app performance, user satisfaction, and feature prioritization to guide product improvement.
2. Methodology & Results by Task
Task 1 — Data Collection & Preprocessing
Methodology:
Phase
Details
Output
Data Collection
Used google-play-scraper Python library to target three package IDs (cbe.mobile, com.bankofabyssinia.app, com.dashenbank.app). Collected ≥400 reviews per bank (text, rating, date, bank name).
data/raw/combined_raw.csv (1,200+ rows)
Preprocessing
Merged raw files; removed duplicates (by ID/text); handled missing data; coerced ratings to integers; normalized dates to YYYY-MM-DD format.
data/processed/clean_reviews.csv
Git Workflow
Code organized under src/scraping and src/preprocessing. Commits managed on the task-1 branch.
Ready dataset

Result: Combined raw reviews: 1,200+ rows. Cleaned dataset ready for subsequent analysis.
Task 2 — Sentiment & Theme Analysis
Methodology:
Analysis Type
Details
Models/Methods
Sentiment
Scored and classified reviews into POSITIVE, NEUTRAL, or NEGATIVE categories.
VADER transformer (90%+ coverage)
Thematic
Extracted keywords using TF-IDF and spaCy, grouped into five primary themes and an 'Other' category.
TF-IDF & spaCy

Results: Sentiment Distribution per Bank
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
Dashen Bank
52
83
175

Results: Theme Counts per Bank
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
Dashen Bank
12
20
17
7
5
249

Task 3 — PostgreSQL Storage
Methodology:
Phase
Details
Tools
Database Setup
Created the bank_reviews PostgreSQL database with defined schema.
PostgreSQL
Schema Definition
Established Banks (bank_id, bank_name) and Reviews (review_id, bank_id FK, review_text, rating, sentiment_label, etc.) tables.
SQL
Data Insertion
Programmatically inserted all 1,200+ cleaned reviews into the database.
Python, psycopg2, SQLAlchemy

Result: Database populated and verified, ready to serve data for analytics and dashboarding.
Task 4 — Insights & Visualization
Objective: To analyze customer reviews to extract meaningful insights on overall sentiment, common themes, average ratings, and visualize trends.
Data Description: Used 970 customer reviews with merged sentiment and theme columns (review_id, rating, bank, sentiment_label, theme, etc.).
Methodology: Data aggregated to calculate average rating, sentiment counts, and theme counts per bank, then visualized using bar plots and heatmaps.
Results:
4.1 Average Rating per Bank
Bank
Average Rating
Bank of Abyssinia (BOA)
3.12
Commercial Bank of Ethiopia (CBE)
3.98
Dashen Bank
3.75

Insight: CBE has the highest overall average customer rating.
4.2 Sentiment Counts per Bank
(Data table identical to Task 2 results)
Insight: Dashen Bank holds the highest count of positive reviews, while BOA has the highest proportional count of negative reviews.
4.3 Theme Counts per Bank
(Data table identical to Task 2 results)
Insight: While the majority of reviews fall under the general "Other" category, Transaction Performance and Account Access are consistently recurring critical issues across the banks.
4.4 Visualizations
Average Rating per Bank (Plot: plots/average_rating_per_bank.png)
Sentiment Distribution per Bank (Plot: plots/sentiment_counts_per_bank.png)
Theme Distribution per Bank (Plot: plots/theme_counts_per_bank.png)
3. Overall Conclusion & Recommendations
The completed four tasks provide a robust foundation for Customer Experience Analytics.
Top Performers: CBE and Dashen Bank show higher customer satisfaction based on superior average ratings and higher positive sentiment counts.
Key Pain Points: The most significant areas for mandatory improvement across all three applications are Account Access and Transaction Performance. These themes are directly linked to core banking app functionality and user frustration.
Actionability: The sentiment and theme visualizations, now backed by a persistent PostgreSQL database, offer actionable data to guide product teams toward specific feature improvements, customer support enhancements, and stability fixes.
4. Appendix
Merged Dataset: data/processed/clean_reviews_with_sentiment_and_themes.csv
Analysis Scripts: src/task_4/insights.py, src/task_4/merge_sentiment.py
Visualization Script: src/task_4/visualizations/insights_plot.py

