"""
    Truth Social API Handler
"""


from dotenv import load_dotenv
from truthbrush import Api
import os
from app.models.models import RawPost
from datetime import datetime

load_dotenv()

TRUTHSOCIAL_USERNAME = os.getenv("TRUTHSOCIAL_USERNAME")
TRUTHSOCIAL_PASSWORD = os.getenv("TRUTHSOCIAL_PASSWORD")

api = Api(username=TRUTHSOCIAL_USERNAME, password=TRUTHSOCIAL_PASSWORD)


def get_posts(user: str, max_posts):
    raw_statuses = api.pull_statuses(user)
        
    statuses = []
    
    for post in raw_statuses:
        statuses.append(post)
        if len(statuses) >= max_posts:
            break
    
    raw_posts: list[RawPost] = []
    
    for status in statuses:

        id: str = status['id']
        date: str = status['created_at']
        timestamp = datetime.fromisoformat(date.replace("Z", "+00:00"))
        username: str  = status['account']['username']
        content: str = status['content']
        

        raw_post = RawPost(
            post_id=id,
            timestamp=timestamp,
            username=username,
            content=content
        )
        raw_posts.append(raw_post)

    return raw_posts
