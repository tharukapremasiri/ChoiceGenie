import gzip, json, csv, argparse

def stream_jsonl_gz(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True, help="Path to meta_*.jsonl.gz")
    ap.add_argument("--out", dest="out_csv", default="data/processed/products.csv", help="Output CSV")
    ap.add_argument("--limit", type=int, default=8000, help="Max rows to write (sample size)")
    args = ap.parse_args()

    out_fields = ["id", "name", "category", "price", "average_rating", "rating_number"]
    written = 0

    with open(args.out_csv, "w", newline="", encoding="utf-8") as fout:
        w = csv.DictWriter(fout, fieldnames=out_fields)
        w.writeheader()

        for i, rec in enumerate(stream_jsonl_gz(args.in_path), start=1):
            title = rec.get("title")
            cat = rec.get("main_category")
            price = rec.get("price")
            avg = rec.get("average_rating")
            num = rec.get("rating_number")

            if not title:
                continue

            row = {
                "id": f"p{i}",   # generate a simple unique product ID
                "name": title.strip(),
                "category": cat or "Unknown",
                "price": price if price is not None else "",
                "average_rating": avg if avg is not None else "",
                "rating_number": num if num is not None else ""
            }
            w.writerow(row)
            written += 1
            if written >= args.limit:
                break

    print(f"✅ Wrote {written} rows → {args.out_csv}")

if __name__ == "__main__":
    main()
