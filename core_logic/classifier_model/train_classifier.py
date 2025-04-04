import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from joblib import dump
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "classifier_training_data.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

# Load CSV
df = pd.read_csv(DATA_PATH)
X = df["text"].tolist()
y = df["label"].tolist()

# Train pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

pipeline.fit(X, y)
dump(pipeline, MODEL_PATH)

print(f"✅ Trained model saved to {MODEL_PATH}")
