from datetime import datetime
import re
import pandas as pd
import kagglehub
import os
from rapidfuzz import process, fuzz
from pprint import pprint


from app.models.models import PostSentiment, Sentiment, PostEntity

# Download latest version
path = kagglehub.dataset_download("alexanderxela/sp-500-companies")
df = pd.read_csv("/Users/ryanliu/.cache/kagglehub/datasets/alexanderxela/sp-500-companies/versions/2/sp500-companies.csv", encoding="latin-1")

alias_map = {}

def build_alias_map(df):
    alias_map = {}

    corporate_suffixes = ["inc", "corp", "corporation", "co", "company"]

    for _, row in df.iterrows():
        name = str(row["Name"]).lower()
        ticker = str(row["Ticker"])

        # Remove punctuation
        clean_name = re.sub(r"[^\w\s]", "", name).strip()  # removes ., commas, etc.

        # Basic company name
        alias_map[clean_name] = ticker

        # Remove corporate suffixes
        short_name = clean_name
        for suffix in corporate_suffixes:
            # Remove suffix only if it’s a separate word at the end
            short_name = re.sub(rf"\b{suffix}\b", "", short_name).strip()

        if short_name:
            alias_map[short_name] = ticker

        # Ticker itself
        alias_map[ticker.lower()] = ticker

    return alias_map

alias_map = build_alias_map(df)

def clean(text: str):
    matches = re.findall(r'\b(?:[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*)*)', text)
    return [m.lower() for m in matches]

def ticker_builder(post: PostSentiment):
    words = clean(post.content)
    print(words)
    tickers = set()
    
    for alias, ticker in alias_map.items():
        if alias in words:
            tickers.add(ticker)
    
    return PostEntity(post_id=post.post_id,
                      timestamp=post.timestamp,
                      username=post.username,
                      content=post.content,
                      sentiment=post.sentiment,
                      tickers=list(tickers)
                     )

def build_all(everything):
    list_of_entities = []
    for thing in everything:
        thingy = ticker_builder(thing)
        list_of_entities.append(thingy)
    return list_of_entities

if __name__ == "__main__":
    content = "Apple and Microsoft Corp are leading tech giants. I love AAPL and MSFT stocks!"
    post_entity = ticker_builder(PostSentiment(
        post_id="1",
        timestamp=datetime(2025, 11, 15, 14, 30, 0) ,
        username="test",
        content=content,
        sentiment=Sentiment(positive=0.9, negative=0.05, neutral=0.05)
    ))
    print(post_entity)
    