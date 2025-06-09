I have built this dta pipeline to try and answer the following question:

Can we statistically validate whether Reddit sentiment moves crypto markets, or if it merely echoes price swings?

What I did
Pulled hourly BTC & ETH prices from the CoinGecko API
Scraped the newest r/Cryptocurrency comments via PRAW
Ran VADER sentiment analysis on each comment
Merged price + sentiment into one tidy time series
displayed the results in Tableau 

Early takeaways
So far, price jumps tend to lead positive sentiment by about an hour, suggesting Redditors talk after the market moves, however the dataset is still small

Next steps
I’m automating the pipeline (cron/loop), collecting weeks of data, and will compute rolling correlation & lag analysis to nail down causality

Why it matters
In data analytics & finance, understanding the lead/lag between social chatter and market action can power better trading signals and sentiment-driven dashboards
