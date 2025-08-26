from datasets import load_dataset

# Reviews (Electronics)
reviews = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023/raw_review_Electronics",
    split="train",
    cache_dir="data/raw/amazon"
)

# Metadata (Electronics)
meta = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023/raw_meta_Electronics",
    split="train",   # use "train" here instead of "full"
    cache_dir="data/raw/amazon"
)

print("Review example:", reviews[0])
print("\nMetadata example:", meta[0])
