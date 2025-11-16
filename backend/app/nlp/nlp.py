""" 
    Combined Pipeline for Harkonnen
"""

from app.api.endpoints import TimeFrame, HarkonnenException
from app.models.models import *
from app.nlp.truth_social import get_posts
from app.nlp.sentiment import get_sentiment_batch
from app.nlp.finance_processing import process_posts
from app.nlp import ErrorCodes


def truth_social_pipeline(username:str, time: TimeFrame) -> PostProcessed:
    """main pipeline using truth social data"""

    # 1. Fetch Post Data
    try:
        raw_posts:list[RawPost] = get_posts(str)
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.SCRAPER_FAIL,
            f"Truth Social scraping failed for {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )

    # 2. Batch process for sentiment
    try:
        sentiment_posts:list[PostSentiment] = get_sentiment_batch(raw_posts)
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.SENTIMENT_FAIL,
            f"Sentiment analysis failed for {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )
    
    # 3. Perform entity retrieval
    try:
        entity_posts:list[PostEntity] = any # TODO: Change Once Completed
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.ENTITY_FAIL,
            f"Entity retrieval failed for {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )
    
    # 4. Perform Financial analysis
    try:
        post_processed:FrontEndReady = process_posts(entity_posts)
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.FINANCE_FAIL,
            f"Financial Analysis Failed for  {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )
    
    return post_processed
    
    

def x_pipeline(username:str, time: TimeFrame) -> PostProcessed:
    """main pipeline using scraped x data"""

    # 1. Fetch Post Data
    try:
        raw_posts:list[RawPost] = ...   ### TODO: Wait for Andrew X Scraper Functions
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.SCRAPER_FAIL,
            f"Truth Social scraping failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )

    # 2. Batch process for sentiment
    try:
        sentiment_posts:list[PostSentiment] = get_sentiment_batch(raw_posts)
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.SENTIMENT_FAIL,
            f"Sentiment analysis failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    # 3. Perform entity retrieval
    try:
        entity_posts:list[PostEntity] = any # TODO: Change Once Completed
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.ENTITY_FAIL,
            f"Entity retrieval failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    # 4. Perform Financial analysis
    try:
        post_processed:FrontEndReady = process_posts(entity_posts)
    except Exception as e:
        raise HarkonnenException(
            500,
            ErrorCodes.FINANCE_FAIL,
            f"Financial Analysis Failed for  {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    return post_processed


