import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import os

# Always use the same products.csv that was exported for RDF
CSV_PATH = "data/processed/products.csv"
MODEL_PATH = "ml/models/content_knn.pkl"

def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    # Load the exact same dataset used in RDF
    df = pd.read_csv(CSV_PATH)

    # Build text features (name + category). Can expand with description later.
    df["text"] = df["name"].fillna("") + " " + df["category"].fillna("")

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["text"])

    # Cosine similarity
    sim = cosine_similarity(X, X)

    # Normalize similarity to [0,1]
    sim = (sim - sim.min()) / (sim.max() - sim.min() + 1e-9)

    # Store IDs, similarity matrix, and vectorizer
    model = {
        "ids": df["id"].tolist(),
        "similarity": sim,
        "vectorizer": vectorizer,
    }

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"✅ Saved content-based similarity model → {MODEL_PATH}")
    print(f"   Trained on {len(df)} products")

if __name__ == "__main__":
    main()
