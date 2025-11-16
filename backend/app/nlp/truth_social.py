"""
    Truth Social API Handler
"""


import json
from dotenv import load_dotenv
from truthbrush import Api
from concurrent.futures import ThreadPoolExecutor
import os
from app.models.models import RawPost
from datetime import datetime
import asyncio

load_dotenv()

TRUTHSOCIAL_USERNAME = os.getenv("TRUTHSOCIAL_USERNAME")
TRUTHSOCIAL_PASSWORD = os.getenv("TRUTHSOCIAL_PASSWORD")

api = Api(username=TRUTHSOCIAL_USERNAME, password=TRUTHSOCIAL_PASSWORD)


def download_posts(username="realDonaldTrump", limit=1000, out_file="trump_posts.json"):
    posts = []
    print(f"Downloading up to {limit} posts for: {username}")

    for i, status in enumerate(api.pull_statuses(username)):
        if i >= limit:
            break
        posts.append(status)

    with open(out_file, "w") as f:
        json.dump(posts, f, indent=2)

    print(f"Saved {len(posts)} posts → {out_file}")


async def get_posts(user: str, max_posts):
    loop = asyncio.get_running_loop()
    raw_statuses = await loop.run_in_executor(None, api.pull_statuses, user)
        
    raw_posts: list[RawPost] = []

    for i, status in enumerate(raw_statuses):
        if i >= max_posts:
            break
        try:
            timestamp = datetime.fromisoformat(status['created_at'].replace("Z", "+00:00"))
            raw_post = RawPost(
                post_id=status['id'],
                timestamp=timestamp,
                username=status['account']['username'],
                content=status['content']
            )
            raw_posts.append(raw_post)
        except Exception as e:
            print(f"Skipping post {status.get('id')} due to error: {e}")

    return raw_posts

if __name__ == "__main__":
    posts = asyncio.run(get_posts("realDonaldTrump", 500))
    with open("trump_posts_500.json", "w") as f:
        json.dump([post.model_dump() for post in posts], f, indent=2, default=str)