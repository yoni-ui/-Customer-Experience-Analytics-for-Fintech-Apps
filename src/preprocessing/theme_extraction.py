import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import os

DATA_FILE = "data/processed/reviews_with_sentiment.csv"
OUT_FILE = "data/processed/reviews_with_themes.csv"
os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv(DATA_FILE)
nlp = spacy.load("en_core_web_sm")

# Function to preprocess text
def preprocess(text):
    doc = nlp(str(text).lower())
    tokens = [t.lemma_ for t in doc if not t.is_stop and t.is_alpha]
    return " ".join(tokens)

df['clean_text'] = df['review'].apply(preprocess)

# Extract keywords using TF-IDF
vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1,2))
X = vectorizer.fit_transform(df['clean_text'])
keywords = vectorizer.get_feature_names_out()

print("Top 20 keywords:", keywords[:20])

# Simple manual theme grouping example (you can adjust)
def assign_theme(text):
    text = str(text)
    if any(k in text for k in ['login', 'password', 'account']):
        return 'Account Access'
    elif any(k in text for k in ['slow', 'lag', 'loading', 'transfer']):
        return 'Transaction Performance'
    elif any(k in text for k in ['crash', 'bug', 'error']):
        return 'App Stability'
    elif any(k in text for k in ['ui', 'design', 'layout', 'navigation']):
        return 'User Interface'
    elif any(k in text for k in ['support', 'customer', 'help']):
        return 'Customer Support'
    else:
        return 'Other'

df['theme'] = df['clean_text'].apply(assign_theme)

# Save to CSV
df.to_csv(OUT_FILE, index=False)
print(f"Saved theme CSV: {OUT_FILE}")
