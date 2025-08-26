from rdflib import Graph, Namespace
import json, os

BASE = "http://example.org/onto#"
EX = Namespace(BASE)

ONTO_PATH = "kg/ttl/ontology.ttl"
DATA_PATH = "kg/ttl/products.ttl"
PREFS_PATH = "data/user_prefs.json"

def _read_json(path):
    if not os.path.exists(path): return {}
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def _write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_prefs(user_id: str):
    prefs = _read_json(PREFS_PATH)
    return prefs.get(user_id, {
        "preferred_categories": [],
        "budget": None,
        "min_rating": 0.0,
        "preferred_brands": []
    })

def save_prefs(user_id: str, new_prefs: dict):
    prefs = _read_json(PREFS_PATH)
    prefs[user_id] = {**load_prefs(user_id), **new_prefs}
    _write_json(PREFS_PATH, prefs)
    return prefs[user_id]

def load_graph() -> Graph:
    g = Graph()
    g.parse(ONTO_PATH, format="turtle")
    g.parse(DATA_PATH, format="turtle")
    return g

def fetch_candidates(g: Graph, limit: int = 4000):
    Q = """
    PREFIX : <http://example.org/onto#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?p ?name ?cat ?catLabel ?price ?rating ?reviewCountVar WHERE {
      ?p a :Product ; :name ?name .
      OPTIONAL { ?p :inCategory ?cat . OPTIONAL { ?cat :name ?catLabel . } }
      OPTIONAL { ?p :price ?price . }
      OPTIONAL { ?p :rating ?rating . }
      OPTIONAL { ?p :reviewCount ?reviewCountVar . }
    } LIMIT %d
    """ % limit

    rows = []
    for r in g.query(Q):
        # Safe parsing: always use str() then cast if possible
        def safe_float(x):
            try: return float(str(x))
            except: return None
        def safe_int(x):
            try: return int(str(x))
            except: return 0

        rows.append({
            "uri": str(r.p),
            "name": str(r.name),
            "category_uri": str(r.cat) if r.cat else None,
            "category": str(r.catLabel) if r.catLabel else None,
            "price": safe_float(r.price) if r.price is not None else None,
            "rating": safe_float(r.rating) if r.rating is not None else None,
            "reviewCount": safe_int(r.reviewCountVar) if r.reviewCountVar is not None else 0
        })
    return rows

def semantic_score(item, prefs):
    """Return (score in [0,1], reasons list)."""
    score = 0.0
    reasons = []

    pref_cats = [c.lower() for c in prefs.get("preferred_categories", []) if c]
    budget = prefs.get("budget")
    min_rating = prefs.get("min_rating", 0.0) or 0.0
    pref_brands = [b.lower() for b in prefs.get("preferred_brands", []) if b]

    # weights sum to 1.0
    W_CAT = 0.40
    W_RAT = 0.30
    W_BUD = 0.20
    W_POP = 0.10

    # Category match
    cat_label = (item.get("category") or "").lower()
    if pref_cats and cat_label in pref_cats:
        score += W_CAT
        reasons.append(f"Matches your {item.get('category')} preference")

    # Rating
    rating = item.get("rating")
    if rating is not None:
        rating_norm = max(0.0, min(rating / 5.0, 1.0))
        score += W_RAT * rating_norm
        if rating >= min_rating:
            reasons.append(f"Highly rated ({rating:.1f}★)")
        else:
            reasons.append(f"Rated {rating:.1f}★")

    # Budget
    price = item.get("price")
    if price is not None and budget:
        if price <= budget:
            fit = max(0.0, (budget - price) / max(budget, 1))
            score += W_BUD * min(1.0, 0.5 + fit)
            reasons.append(f"Within your budget (≤ {budget})")
        else:
            over = (price - budget) / max(budget, 1)
            near = max(0.0, 1.0 - over)
            score += W_BUD * (0.2 * near)
            reasons.append(f"Above budget ({price} > {budget})")

    # Popularity
    rc = int(item.get("reviewCount") or 0)
    if rc > 0:
        pop = min(rc / 1000.0, 1.0)
        score += W_POP * pop
        reasons.append(f"{rc} review(s)")

    return max(0.0, min(score, 1.0)), reasons

def rank_items(items, prefs, k=10):
    ranked = []
    for it in items:
        s, reasons = semantic_score(it, prefs)
        it2 = {**it, "semantic_score": s, "reasons": reasons, "explanation": "; ".join(reasons)}
        ranked.append(it2)

    # Filter by min_rating
    min_rating = prefs.get("min_rating") or 0.0
    if min_rating:
        ranked = [r for r in ranked if (r.get("rating") or 0) >= min_rating]

    # Stable-sort: preferred categories first
    pref_cats = [c.lower() for c in prefs.get("preferred_categories", [])]
    if pref_cats:
        def cat_key(x):
            cat = (x.get("category") or "").lower()
            return 0 if cat in pref_cats else 1
        ranked.sort(key=lambda x: (-x["semantic_score"], cat_key(x)))
    else:
        ranked.sort(key=lambda x: -x["semantic_score"])

    return ranked[:k]
