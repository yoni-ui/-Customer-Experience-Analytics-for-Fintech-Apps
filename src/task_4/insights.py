# File: src/task_4/insights.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load cleaned data from Task 1
cleaned_data_path = "data/processed/clean_reviews.csv"
df = pd.read_csv(cleaned_data_path)

print(f"Loaded {len(df)} reviews")
print(df.head())

# Average rating per bank
avg_rating = df.groupby('bank')['rating'].mean()
print("\nAverage rating per bank:")
print(avg_rating)

# Sentiment distribution per bank
sentiment_counts = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
print("\nSentiment counts per bank:")
print(sentiment_counts)

# Top themes per bank
themes_summary = df.groupby(['bank', 'identified_theme']).size().unstack(fill_value=0)
print("\nThemes summary per bank:")
print(themes_summary)
# File: src/task_4/insights.py

from visualizations.plots import plot_sentiment_distribution, plot_average_rating, generate_wordcloud

# Plot average rating
plot_average_rating(avg_rating)

# Plot sentiment distribution
plot_sentiment_distribution(sentiment_counts)

# Generate WordCloud for all reviews per bank
for bank in df['bank'].unique():
    bank_text = df[df['bank'] == bank]['review'].dropna().tolist()
    generate_wordcloud(bank_text, title=f"WordCloud - {bank}")
# Top keywords per theme
top_keywords = df.groupby('identified_theme')['review'].apply(lambda x: " ".join(x).split())
for theme, words in top_keywords.items():
    print(f"\nTop words for theme '{theme}':")
    freq = pd.Series(words).value_counts().head(10)
    print(freq)

plt.savefig(f"reports/{bank}_sentiment.png")
