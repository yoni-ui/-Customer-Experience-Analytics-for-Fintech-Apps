# File: src/task_4/visualizations/plots.py

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def plot_sentiment_distribution(sentiment_df):
    sentiment_df.plot(kind='bar', stacked=True, figsize=(10,6))
    plt.title("Sentiment Distribution per Bank")
    plt.ylabel("Number of Reviews")
    plt.xlabel("Bank")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def plot_average_rating(avg_rating):
    avg_rating.plot(kind='bar', color='skyblue', figsize=(8,5))
    plt.title("Average Rating per Bank")
    plt.ylabel("Rating")
    plt.ylim(0,5)
    plt.xlabel("Bank")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def generate_wordcloud(text, title="WordCloud"):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(text))
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.show()
plt.savefig(f"reports/{bank}_sentiment.png")
