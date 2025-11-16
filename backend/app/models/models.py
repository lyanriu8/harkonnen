from pydantic import BaseModel, Field, confloat
from datetime import datetime
from typing import List


# ----------------------
# 1. Raw scraped post
# ----------------------
class RawPost(BaseModel):
    post_id: str
    timestamp: datetime
    username: str
    content: str


# ----------------------
# 2. Sentiment
# ----------------------
class Sentiment(BaseModel):
    positive: float
    negative: float
    neutral: float


class PostSentiment(RawPost):         
    sentiment: Sentiment


# ----------------------
# 3. Entity extraction
# ----------------------
class PostEntity(PostSentiment):        
    tickers: List[str]


# ----------------------
# 4. Financial analysis
# ----------------------
class PriceChanges(BaseModel):
    ticker: str
    one_day: float
    seven_day: float
    one_day_percent: float
    seven_day_percent: float    


class PostProcessed(PostEntity):
    price_changes: List[PriceChanges]

class FrontEndReady(BaseModel):
    one_day_influence_score: float
    seven_day_influence_score: float
    posts: List[PostProcessed]