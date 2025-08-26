from flask import Flask, request, jsonify
from semantic import load_graph, fetch_candidates, load_prefs, save_prefs, rank_items, semantic_score
from ml_helper import predict_content_score, IDS



app = Flask(__name__)
G = load_graph()  # load once at startup

@app.get("/health")
def health():
    return {"status": "ok", "triples": len(G)}, 200

@app.post("/preferences")
def set_prefs():
    data = request.get_json(force=True) or {}
    user = data.get("user", "u1")
    new_prefs = {k: data.get(k) for k in ["preferred_categories", "budget", "min_rating", "preferred_brands"] if k in data}
    out = save_prefs(user, new_prefs)
    return jsonify({"user": user, "preferences": out})

@app.get("/preferences")
def get_prefs():
    user = request.args.get("user", "u1")
    return jsonify({"user": user, "preferences": load_prefs(user)})

@app.get("/recommendations")
def recommendations():
    user = request.args.get("user", "u1")
    k = int(request.args.get("k", 10))
    prefs = load_prefs(user)

    items = fetch_candidates(G, limit=4000)
    ranked = []
    liked_ids = prefs.get("liked_items", [])

    for it in items:
        # Step 1: compute semantic score
        s, reasons = semantic_score(it, prefs)
        it["semantic_score"] = round(s, 3)
        it["reasons"] = reasons

        # Step 2: compute ML score (content-based similarity)
        item_id = it["uri"].split("#")[-1]
        ml_score = predict_content_score(item_id, liked_ids)
        it["ml_score"] = round(ml_score, 3)

        # Step 3: blend scores (hybrid)
        final_score = 0.5 * s + 0.5 * ml_score  # balanced weights
        it["final_score"] = round(final_score, 3)

        # Step 4: explanations
        extra_reasons = reasons[:]
        if ml_score > 0.1:  # only show if meaningful
            extra_reasons.append("Similar to items you viewed/liked")

        it["explanation"] = "; ".join(extra_reasons)
        ranked.append(it)

        print("Candidate:", item_id, "In model:", item_id in IDS)


    # Sort by hybrid score
    ranked.sort(key=lambda x: -x["final_score"])
    return jsonify(ranked[:k])




if __name__ == "__main__":
    app.run(debug=True)
