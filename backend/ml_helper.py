import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("ml", "models", "content_knn.pkl")

# Load model once at startup
if os.path.exists(MODEL_PATH):
    MODEL = joblib.load(MODEL_PATH)
    SIM = MODEL["similarity"]
    IDS = MODEL["ids"]
else:
    MODEL, SIM, IDS = None, None, []

def predict_content_score(item_id: str, liked_ids=None, topn=10):
    """Return similarity score ∈ [0,1] for this item given user liked_ids."""
    if MODEL is None or liked_ids is None or len(liked_ids) == 0:
        return 0.0

    if item_id not in IDS:
        return 0.0
    idx = IDS.index(item_id)

    # collect sims with all liked_ids
    sims = []
    for lid in liked_ids:
        if lid in IDS:
            lidx = IDS.index(lid)
            sims.append(SIM[lidx, idx])
    if not sims:
        return 0.0
    return float(np.mean(sims))  # normalize already [0..1]
