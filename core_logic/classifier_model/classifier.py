from joblib import load
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

classifier = load(MODEL_PATH)

def classify_intent(text: str) -> str:
    return classifier.predict([text])[0]
