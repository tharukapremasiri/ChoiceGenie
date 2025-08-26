import gzip, json

path = "data/raw/amazon/meta_Electronics.jsonl.gz"

with gzip.open(path, "rt", encoding="utf-8") as f:
    for i, line in enumerate(f):
        rec = json.loads(line)
        print(json.dumps(rec, indent=2)[:500])  # show first 500 chars
        if i >= 2:  # just first 3 records
            break
