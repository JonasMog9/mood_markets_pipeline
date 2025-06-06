"""
merge_to_processed.py
---------------------

Reads:
  • data/raw/crypto_prices.csv
  • data/raw/reddit_sentiment.csv

Produces:
  • data/processed/mood_market.csv   (one row per hour * per coin*)
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- 1. Read the two source files ----------
prices = pd.read_csv(RAW_DIR / "crypto_prices.csv", parse_dates=["timestamp_utc"])
sent   = pd.read_csv(RAW_DIR / "reddit_sentiment.csv", parse_dates=["timestamp_utc"])

# round both to the *hour* just in case
prices["timestamp_utc"] = prices["timestamp_utc"].dt.floor("h")
sent["timestamp_utc"]   = sent["timestamp_utc"].dt.floor("h")

# ---------- 2. Merge on timestamp ----------
merged = prices.merge(sent, on="timestamp_utc", how="inner")

# ---------- 3. Save ----------
out_path = OUT_DIR / "mood_market.csv"
merged.to_csv(out_path, index=False)

print(f"✅  Wrote {len(merged):,} rows  →  {out_path}")
