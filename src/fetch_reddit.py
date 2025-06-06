"""
fetch_reddit.py
---------------

• Grabs the newest comments from r/Cryptocurrency (last ~100 per run)
• Filters out super-short or low-score comments (noise)
• Scores each comment with VADER sentiment
• Resamples to *hourly* average sentiment
• Appends result to data/raw/reddit_sentiment.csv


"""

import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

import pandas as pd
import praw
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------- 0. Setup ----------
load_dotenv()                                    # read .env keys
analyser = SentimentIntensityAnalyzer()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET") or None,  # blank allowed
    user_agent=os.getenv("REDDIT_USER_AGENT", "mood-app"),
)

# ---------- 1. Pull fresh comments ----------
utc_now = datetime.now(timezone.utc)
utc_1h_ago = utc_now - timedelta(hours=1)

comments_data = []
sub = reddit.subreddit("cryptocurrency")
for comment in sub.comments(limit=200):         # ~2 API calls
    ts = datetime.fromtimestamp(comment.created_utc, tz=timezone.utc)
    if ts < utc_1h_ago:
        break                                   # comments are ordered newest→oldest
    # basic noise filter
    if len(comment.body) < 20 or comment.score < 1:
        continue
    score = analyser.polarity_scores(comment.body)["compound"]
    comments_data.append(
        {"timestamp_utc": ts.replace(minute=0, second=0, microsecond=0),
         "sentiment": score}
    )

if not comments_data:
    print("No qualifying comments in the last hour. Nothing to write.")
    raise SystemExit

# ---------- 2. Average to one row per hour ----------
df = pd.DataFrame(comments_data)
hourly = (df.groupby("timestamp_utc")["sentiment"]
            .mean()                      # average score
            .reset_index())

# ---------- 3. Append to CSV ----------
csv_path = Path("data/raw/reddit_sentiment.csv")
new_file = not csv_path.exists()
hourly.to_csv(csv_path, mode="a",
              index=False,
              header=new_file)

print(f"✅  Added {len(hourly)} hourly rows → {csv_path}")
