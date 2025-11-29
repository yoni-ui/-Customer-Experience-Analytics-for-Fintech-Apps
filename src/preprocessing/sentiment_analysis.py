import pandas as pd
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

DATA_FILE = "data/processed/clean_reviews.csv"
OUT_FILE = "data/processed/reviews_with_sentiment.csv"
os.makedirs("data/processed", exist_ok=True)

# Load clean reviews
df = pd.read_csv(DATA_FILE)

# Initialize models
hf_sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
vader = SentimentIntensityAnalyzer()

def get_hf_sentiment(text):
    result = hf_sentiment(text[:512])[0]  # limit to first 512 tokens
    return result['label'], result['score']

def get_vader_sentiment(text):
    score = vader.polarity_scores(text)['compound']
    if score >= 0.05:
        return "POSITIVE", score
    elif score <= -0.05:
        return "NEGATIVE", -score
    else:
        return "NEUTRAL", abs(score)

# Choose either HF or VADER
labels = []
scores = []

for review in df['review']:
    label, score = get_vader_sentiment(str(review))
    labels.append(label)
    scores.append(score)

df['sentiment_label'] = labels
df['sentiment_score'] = scores

# Save to CSV
df.to_csv(OUT_FILE, index=False)
print(f"Saved sentiment CSV: {OUT_FILE}")
