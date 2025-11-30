import pandas as pd

cleaned_data_path = "data/processed/clean_reviews_with_sentiment_and_themes.csv"
df = pd.read_csv(cleaned_data_path)
df.columns = df.columns.str.strip()  # remove whitespace

print(f"Loaded {len(df)} reviews")
print("Columns:", df.columns.tolist())

# Use the correct columns from merged CSV
rating_col = "rating_y"
sentiment_col = "sentiment_label_y"
theme_col = "theme"

# Average rating per bank
avg_rating = df.groupby("bank")[rating_col].mean()
print("\nAverage rating per bank:")
print(avg_rating)

# Sentiment counts per bank
sentiment_counts = df.groupby(["bank", sentiment_col]).size().unstack(fill_value=0)
print("\nSentiment counts per bank:")
print(sentiment_counts)

# Theme counts per bank
themes_summary = df.groupby(["bank", theme_col]).size().unstack(fill_value=0)
print("\nTheme counts per bank:")
print(themes_summary)
