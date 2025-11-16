""" 
    Combined Pipeline for Harkonnen
"""

from app.api.endpoints import TimeFrame, HarkonnenException
from app.models.models import *
from app.nlp.truth_social import get_posts
from app.nlp.sentiment import get_sentiment_batch
from app.nlp.finance_processing import process_posts
from app.tools.twitter_scraper.interpreter import get_tweets
from app.nlp.semantic_search import append_rag_results
from app.nlp import ErrorCodes
from app.nlp.fuzzy import build_all

def truth_social_pipeline(username:str, limit: int) -> PostProcessed:
    """main pipeline using truth social data"""

    # 1. Fetch Post Data
    try:
        raw_posts:list[RawPost] = get_posts(username, limit)
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.SCRAPER_FAIL),
            f"Truth Social scraping failed for {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )

    # 2. Batch process for sentiment
    try:
        sentiment_posts:list[PostSentiment] = get_sentiment_batch(raw_posts)
        sentiment_posts = [
            post for post in sentiment_posts
            if post.sentiment.positive >= 0.33 or post.sentiment.negative >= 0.33
        ]
            
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.SENTIMENT_FAIL),
            f"Sentiment analysis failed for {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )
    
    # 3. Perform entity retrieval
    try:
        entity_posts:list[PostEntity] = build_all(sentiment_posts)
        if entity_posts is None:
            print(f"No posts found")
            return FrontEndReady(posts=[])
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.ENTITY_FAIL),
            f"Entity retrieval failed for {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )
    
    # 4. Perform Financial analysis
    try:
        post_processed:FrontEndReady = process_posts(entity_posts)
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.FINANCE_FAIL),
            f"Financial Analysis Failed for  {username}",
            {"platform": "truth_social", "username": username, "error": str(e)}
        )
    
    return post_processed
    
    

def x_pipeline(username:str, limit:int) -> PostProcessed:
    """main pipeline using scraped x data"""

    # 1. Fetch Post Data
    try:
        raw_posts:list[RawPost] = get_tweets(username, limit)   ### TODO: Wait for Andrew X Scraper Functions
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.SCRAPER_FAIL),
            f"Truth Social scraping failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )

    # 2. Batch process for sentiment
    try:
        sentiment_posts:list[PostSentiment] = get_sentiment_batch(raw_posts)
        sentiment_posts = [
            post for post in sentiment_posts
            if post.sentiment.positive >= 0.33 or post.sentiment.negative >= 0.33
        ]
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.SENTIMENT_FAIL),
            f"Sentiment analysis failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    # 3. Perform entity retrieval
    try:
        entity_posts:list[PostEntity] = build_all(sentiment_posts)
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.ENTITY_FAIL),
            f"Entity retrieval failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    # 4. RAG Query
    try:
        entity_post_plus_rag:list[PostEntity] = append_rag_results(entity_posts, 3)
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.RAG_FAIL),
            f"Entity retrieval augmented generation failed for {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    # 5. Perform Financial analysis
    try:
        post_processed:FrontEndReady = process_posts(entity_post_plus_rag)
    except Exception as e:
        raise HarkonnenException(
            500,
            str(ErrorCodes.FINANCE_FAIL),
            f"Financial Analysis Failed for  {username}",
            {"platform": "X", "username": username, "error": str(e)}
        )
    
    return post_processed


