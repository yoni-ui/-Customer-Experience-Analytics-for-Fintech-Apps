import pandas as pd

# Correct paths to existing files
clean_reviews_path = "data/processed/clean_reviews.csv"
sentiment_path = "data/processed/sentiment_results.csv"
themes_path = "data/processed/reviews_with_themes.csv"

# Load CSVs
df_clean = pd.read_csv(clean_reviews_path)
df_sentiment = pd.read_csv(sentiment_path)
df_themes = pd.read_csv(themes_path)

# Merge sentiment into clean reviews
df_merged = df_clean.merge(df_sentiment, on="review_id", how="left")

# Merge themes
df_merged = df_merged.merge(df_themes, on="review_id", how="left")

# Save final merged CSV for insights
merged_path = "data/processed/clean_reviews_with_sentiment_and_themes.csv"
df_merged.to_csv(merged_path, index=False)
print(f"Merged data saved to {merged_path}")
