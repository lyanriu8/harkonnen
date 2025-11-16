from dotenv import load_dotenv
from truthbrush import Api
import os
from models import RawPost

load_dotenv()

TRUTHSOCIAL_USERNAME = os.getenv("TRUTHSOCIAL_USERNAME")
TRUTHSOCIAL_PASSWORD = os.getenv("TRUTHSOCIAL_PASSWORD")

api = Api(username=TRUTHSOCIAL_USERNAME, password=TRUTHSOCIAL_PASSWORD)



user = "realDonaldTrump"
statuses = api.pull_statuses(user)

def get_posts(user: str):
    statuses = api.pull_statuses(user)
    raw_posts: RawPost = []
    for status in statuses:

        id: str = status['id']
        date: str = status['created_at']
        username: str  = status['account']['username']
        content: str = status['content']
        
        raw_post = RawPost(
            post_id=id,
            timestamp=date,
            username=username,
            content=content
        )
        raw_posts.append(raw_post)

    return raw_posts
