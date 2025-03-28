# -*- coding: utf-8 -*-
"""Twitter Sentiment Analysis:Naive Bayes Classifier.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sulBCMLMZcnyp-zYF58PVXjFvN9kTkcc
"""

import kagglehub

# Download latest version
path = kagglehub.dataset_download("kazanova/sentiment140")

print("Path to dataset files:", path)

import pandas as pd
import os

dataset_path = "/root/.cache/kagglehub/datasets/kazanova/sentiment140/versions/2"
os.listdir(dataset_path)

file_path = os.path.join(dataset_path, "training.1600000.processed.noemoticon.csv")

df = pd.read_csv(file_path, encoding='latin-1', header=None)

df.head()

df.columns = ["target", "id", "date", "flag", "user", "text"]

df.head()

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
nltk.data.path.append('/usr/local/nltk_data')
# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

print(os.listdir(nltk.data.find("tokenizers")))
print(os.listdir(nltk.data.find("corpora")))

def clean_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions (@user)
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    text = text.strip()  # Trim whitespace
    words = word_tokenize(text)  # Tokenize
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    return ' '.join(words)

# Apply cleaning
df['text'] = df['text'].apply(clean_text)

X = df['text']  # Features (tweets)
y = df['target']  # Labels (sentiment)

# Train-test split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a pipeline (TF-IDF + Naive Bayes)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1,2))),
    ('clf', MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

# Accuracy
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Classification Report
print(classification_report(y_test, y_pred))

sample_tweets = ["I love this product!", "This is the worst experience ever."]
predictions = pipeline.predict(sample_tweets)

for tweet, sentiment in zip(sample_tweets, predictions):
    print(f"Tweet: {tweet} --> Sentiment: {'Positive' if sentiment == 1 else 'Negative'}")