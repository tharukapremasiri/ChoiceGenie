import joblib

MODEL_PATH = "ml/models/content_knn.pkl"
model = joblib.load(MODEL_PATH)

SIM = model["similarity"]
IDS = model["ids"]

test_id = "p1721"
if test_id in IDS:
    idx = IDS.index(test_id)
    sims = list(enumerate(SIM[idx]))
    sims_sorted = sorted(sims, key=lambda x: -x[1])
    for i, score in sims_sorted[:10]:
        print(IDS[i], score)
