"""
    Client endpoints for API service + debugging
"""

from fastapi import APIRouter, Query
from typing import Dict, Any
from app.models.models import *
from app.api.endpoints import TimeFrame, HarkonnenException
from app.nlp.sentiment import get_sentiment
from app.nlp.rag.query_rag import RagStore
from app.nlp import ErrorCodes


sub_router = APIRouter(tags=["Client"])

# ----- Sentiment -----

@sub_router.get("/nlp/sentiment/single", response_model=Sentiment)
def get_single_sentiment(content: str):
    """Run Finbert sentiment analysis on a single String"""
    try :
         sent:Sentiment = get_sentiment(str)
    except Exception as e:
            raise HarkonnenException(
                500,
                str(ErrorCodes.SENTIMENT_FAIL),
                f"RAG FAILED",
                {"platform": "nil", "username": "client-single", "error": str(e)}
    )

    return sent
    

@sub_router.post("/nlp/sentiment/batch", response_model=list[Sentiment])
def get_multiple_sentiment(contents: list[str]):
    sents:list[Sentiment] = []
    for c in contents:
        try :
            sent:Sentiment = get_sentiment(c)
        except Exception as e:
                raise HarkonnenException(
                    500,
                    str(ErrorCodes.SENTIMENT_FAIL),
                    f"RAG FAILED",
                    {"platform": "nil", "username": "client-single", "error": str(e)}
        )
        sents.append(sent)

    return sents
         
        


# ----- Entities -----
@sub_router.get("/nlp/entity/single/{content}", response_model=list[str])
def get_entities_for_single_post(content: str, k: int):
    """return a relvant list of tickers for a single string of content"""
    rag = RagStore()
    try :
        results = rag.search(content, k)
        ret = []
        for r in results:
            ret.append(r["ticker"])
    except Exception as e:
            raise HarkonnenException(
                500,
                str(ErrorCodes.RAG_FAIL),
                f"RAG FAILED",
                {"platform": "nil", "username": "client-single", "error": str(e)}
    )
    
    return ret


@sub_router.post("/nlp/entity/batch", response_model=list[list[str]])
def get_entities_for_multiple_posts(contents: list[str], k: int):
    """Return list of relevant entities/tickers for a list a content"""
    rag = RagStore()
    rets = []
    for content in contents:
        ret = []
        try:
            ret.append(rag.search(content, k))
        except Exception as e:
            raise HarkonnenException(
                500,
                str(ErrorCodes.RAG_FAIL),
                f"RAG FAILED",
                {"platform": "nil", "username": "client-batch", "error": str(e)}
            )
        rets.append(ret)
    return rets


