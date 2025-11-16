"""
    Sub router dedicated to Harkonnen's frontend dashboard
"""

from fastapi import APIRouter, Query
from app.models.models import *
from app.api.endpoints import TimeFrame, HarkonnenException

from app.nlp.nlp import truth_social_pipeline, x_pipeline

sub_router = APIRouter()

@sub_router.get("/process/ts/{influencer}", response_model= FrontEndReady)
def process_batch_ts(influencer:str, limit: int = Query(20, ge=1, le=500)):
    """process a batch of influencer, with a given limit and timeframe for TS"""
    return truth_social_pipeline(influencer, limit)



@sub_router.get("/process/x/{influencer}", response_model= FrontEndReady)
def process_batch_x(influencer:str, timeframe:TimeFrame = TimeFrame.ONE_MONTH, limit: int = Query(20, ge=1, le=200)):
    """process a batch of influencer, with a given limit and timeframe for X"""
    # TODO: X PIPELINE IMPLEMENTATION
    return x_pipeline(str)
    