import json
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from app.models.models import *
from app.api.endpoints import TimeFrame

KEY_CONTENT = "content" # content:str
KEY_AUTHOR = "author"   # author:str
KEY_DATE = "date"       # date:str (UTC standard)

# loads the corresponding json file based on inputted user_handle
# if no corresponding json, return empty dictionary
def load_json(user_handle:str) -> dict[str, any]:
    try:
        with open(f"app/data/twitter_scraper/{user_handle}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# returns a users posts in the last 'days' days
def get_tweets(user_handle:str, days:int) -> list[RawPost]:
    posts = load_json(user_handle.lower())
    out = []
    today = date.today()
    for post_id in posts.keys():
        timestamp = datetime.fromisoformat(posts[post_id][KEY_DATE].replace("Z", "+00:00"))
        oldest = today - relativedelta(days=days)
        if timestamp.date() < oldest: # stop adding to the array if past date limit (dict should be ordered based on date)
            break
        
        content = posts[post_id][KEY_CONTENT]
        if content is None:
            continue
        username = posts[post_id][KEY_AUTHOR]
        out.append(RawPost(post_id=post_id, timestamp=timestamp, username=username, content=content))
    return out