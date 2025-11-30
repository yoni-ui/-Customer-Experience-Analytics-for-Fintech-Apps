import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load merged data
cleaned_data_path = "data/processed/clean_reviews_with_sentiment_and_themes.csv"
df = pd.read_csv(cleaned_data_path)

# Set seaborn style
sns.set(style="whitegrid")

# 1️⃣ Average Ratings per Bank
if 'rating_y' in df.columns:
    avg_rating = df.groupby("bank")["rating_y"].mean().sort_values()
    plt.figure(figsize=(8,5))
    sns.barplot(x=avg_rating.index, y=avg_rating.values, palette="viridis")
    plt.title("Average App Rating per Bank")
    plt.ylabel("Average Rating")
    plt.xlabel("Bank")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("plots/average_rating_per_bank.png")
    plt.show()

# 2️⃣ Sentiment Counts per Bank
if 'sentiment_label_y' in df.columns:
    sentiment_counts = df.groupby(['bank', 'sentiment_label_y']).size().unstack(fill_value=0)
    sentiment_counts.plot(kind='bar', stacked=True, figsize=(10,6), colormap="coolwarm")
    plt.title("Sentiment Distribution per Bank")
    plt.ylabel("Number of Reviews")
    plt.xlabel("Bank")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("plots/sentiment_counts_per_bank.png")
    plt.show()

# 3️⃣ Theme Counts per Bank
if 'theme' in df.columns:
    theme_counts = df.groupby(['bank', 'theme']).size().unstack(fill_value=0)
    theme_counts.plot(kind='bar', stacked=True, figsize=(12,7), colormap="tab20")
    plt.title("Theme Counts per Bank")
    plt.ylabel("Number of Reviews")
    plt.xlabel("Bank")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("plots/theme_counts_per_bank.png")
    plt.show()
