from __future__ import annotations
import argparse
import logging
import sys
import yfinance as yf
from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Any, Dict
import pandas as pd
from app.models.models import PostEntity, PostProcessed, PriceChanges, FrontEndReady
# !!!! call process_posts(List[PostEntity]) from outside this module !!!!
# !!!! receives FrontEndReady object with all data filled in !!!!


# !!! put fix for if post was made wihtin seven days
APP_NAME = "Ticker Processor"
VERSION = "0.1.0"

# -------------------------
# Logging
# -------------------------
def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


# -------------------------
# Core transformation
# -------------------------
def transform_list(posts: List[PostEntity]) -> FrontEndReady:
    one_day_predicts_total = 0
    seven_day_predicts_total = 0
    processed_posts = []
    total_tickers = 0
    for post in posts:
        processed_post, one_day_predicts, seven_day_predicts, ticker_count = transform_post(post)
        one_day_predicts_total += one_day_predicts
        seven_day_predicts_total += seven_day_predicts
        total_tickers += ticker_count
        processed_posts.append(processed_post)
    one_day_influence_score = one_day_predicts_total / total_tickers if posts else 0.0 
    seven_day_influence_score = seven_day_predicts_total / total_tickers if posts else 0.0

    out = FrontEndReady(
            one_day_influence_score=one_day_influence_score,
            seven_day_influence_score=seven_day_influence_score,
            posts=processed_posts 
        )

    return out


def transform_post(post: PostEntity) -> tuple[PostProcessed, int, int, int]: # this is going to 1. provide price_changes for each ticker, 2. return number of true predicts (for each ticker)
    price_changes = [] # one change fr eaach tiker
    total_seven_predicts = 0
    total_one_predicts = 0
    ticker_count = 0
    if post.sentiment.positive >= 0.3:
        sentiment = "positive"
    elif post.sentiment.negative >= 0.3:
        sentiment = "negative"
    else:
        sentiment = ""
    dt = post.timestamp # time of post
    if dt.tzinfo is None:  # naive
        dt = dt.replace(tzinfo=timezone.utc)
    days_ago = (datetime.now(timezone.utc) - dt).days # how many days ago was ts
    interval = "2m" if days_ago <= 50 else "1d" # if within 50 days (60 days hard cutoff - 7days and then safety padding), then 2min, otherwise 1d
    start_date = dt - pd.Timedelta(days=1) # one day before
    end_date = dt + pd.Timedelta(days=10) # ten days later for more leeway
    
    if days_ago <= 7:   # if within 7 days, just do nothing lmao
        processed_post = PostProcessed(
        post_id=post.post_id,
        timestamp=post.timestamp,
        username=post.username,
        content=post.content,
        sentiment=post.sentiment,
        tickers=post.tickers,
        price_changes=None
        )
        return processed_post, 0, 0, 0

    for ticker in post.tickers:
        ticker_count += 1
        
        
        ticker_data = yf.Ticker(ticker).history(start=start_date, end=end_date, interval=interval) # this spits out open, close for each two minutes within time frame, or by day bepeding on interbal

        if ticker_data.empty:
            logging.warning(f"No data found for ticker {ticker}")
            continue
        
        ticker_data.index = ticker_data.index.tz_convert('UTC')
        original_price = get_nearest_price(dt, ticker_data) # should get price at time of post
        if original_price is None:
            logging.warning(f"Could not get original price for {ticker}")
            continue
        price_24h = get_nearest_price(dt + pd.Timedelta(hours = 24), ticker_data)
        price_7d = get_nearest_price(dt + pd.Timedelta(hours = 168), ticker_data)
        if price_24h is None or price_7d is None:
            logging.warning(f"Could not get future prices for {ticker}")
            continue
       
        one_day_change = price_24h - original_price
        seven_day_change = price_7d - original_price

        if sentiment:
            if (sentiment == "positive" and one_day_change > 0) or (sentiment == "negative" and one_day_change < 0):
                total_one_predicts += 1
            if (sentiment == "positive" and seven_day_change > 0) or (sentiment == "negative" and seven_day_change < 0):
                total_seven_predicts += 1
            
        price_change = PriceChanges(ticker=ticker,
                                    one_day=one_day_change,
                                    seven_day=seven_day_change,
                                    one_day_percent=one_day_change/original_price * 100,
                                    seven_day_percent=seven_day_change/original_price * 100,)
        price_changes.append(price_change)

    processed_post = PostProcessed(
        post_id=post.post_id,
        timestamp=post.timestamp,
        username=post.username,
        content=post.content,
        sentiment=post.sentiment,
        tickers=post.tickers,
        price_changes=price_changes
    )

    return processed_post, total_one_predicts, total_seven_predicts, ticker_count

        

def get_nearest_price(target_time: int, ticker_data: pd.DataFrame):
    if target_time < ticker_data.index[0]:
            return None
    nearest_idx = ticker_data.index.get_indexer([target_time], method='ffill')[0]
    return ticker_data.iloc[nearest_idx]['Close']


def process_posts(posts: List[PostEntity], verbose: bool = False) -> FrontEndReady:
    setup_logging(verbose)
    logging.info("Starting %s - Processing %d posts", APP_NAME, len(posts))
    
    result = transform_list(posts)
    
    logging.info("Finished successfully - Processed %d posts", len(result.posts))
    return result

def main(argv=None) -> int:  
    logging.info("Starting %s", APP_NAME)

    example_posts = [
    PostEntity(
        post_id="p001",
        timestamp=datetime(2025, 11, 10, 15, 30),
        username="user_alpha",
        content="I think $AAPL is going to rally this week.",
        sentiment={"positive": 0.8, "negative": 0.1, "neutral": 0.1},
        tickers=["AAPL"]
    ),
    PostEntity(
        post_id="p002",
        timestamp=datetime(2025, 11, 13, 9, 45),
        username="user_beta",
        content="Not confident about $TSLA after recent news.",
        sentiment={"positive": 0.1, "negative": 0.7, "neutral": 0.2},
        tickers=["TSLA"]
    ),
    PostEntity(
        post_id="p003",
        timestamp=datetime(2025, 11, 12, 9, 30),
        username="user_gamma",
        content="$GOOGL seems stable, might be a good hold.",
        sentiment={"positive": 0.2, "negative": 0.2, "neutral": 0.8},
        tickers=["GOOGL", "TSLA", "AMD"]
    ),
]
    processed_data = process_posts(example_posts, verbose=True)
    logging.info("Did not do anything since this is just a module")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))