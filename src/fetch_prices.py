"""
fetch_prices.py
---------------

Pulls the current USD price for Bitcoin and Ethereum from CoinGecko
and appends a timestamped row to data/raw/crypto_prices.csv.

Run it with:
    python src/fetch_prices.py
"""

import requests
import csv
from pathlib import Path
from datetime import datetime, timezone

# Coins we care about (“id” values are CoinGecko’s labels)
COINS = ["bitcoin", "ethereum"]

# -------- 1. Call the API --------
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": ",".join(COINS),
    "vs_currencies": "usd",
}
resp = requests.get(url, params=params, timeout=10)
resp.raise_for_status()                      # will crash loudly on bad response
prices = resp.json()                         # → {'bitcoin': {'usd': 68510}, ...}

# -------- 2. Prepare a row for each coin --------
timestamp = (
    datetime.now(timezone.utc)
    .replace(second=0, microsecond=0)
    .isoformat()
)                                            # e.g. 2025-06-06T17:05:00+00:00

rows = [
    {"timestamp_utc": timestamp, "coin": coin.upper(), "price_usd": prices[coin]["usd"]}
    for coin in COINS
]

# -------- 3. Append to CSV, create header if file doesn’t exist --------
csv_path = Path("data/raw/crypto_prices.csv")
new_file = not csv_path.exists()

with csv_path.open("a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["timestamp_utc", "coin", "price_usd"])
    if new_file:
        writer.writeheader()
    writer.writerows(rows)

print(f"✅  Added {len(rows)} rows @ {timestamp}  →  {csv_path}")
