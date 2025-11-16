# INTERNAL TOOL FOR PARSING AN HTML FILE SAVED FROM SOMEONE'S TWITTER PROFILE -> TO A JSON FILE THAT WILL BE READ BY interpreter.py
# also saves a MASTER file for if we want to continue adding posts from the same user's profile
# make sure to format the html file first using vscode... perhaps ill think of a better way later

import os
import re
import json

##############################################################################
## PARSE
##############################################################################
FILE_PATH = "nasa18.html" # CHANGE THIS TO THE FILE YOU WANT TO PARSE

OUTPUT_PATH = "data/twitter_scraper/"
OUTPUT_MASTER = "nasa"

# nested dictionary for storing tweet contents
# keys - post id
tweet_contents = {}
# nested keys
KEY_CONTENT = "content" # content:str
KEY_AUTHOR = "author"   # author:str
KEY_DATE = "date"       # date:str (UTC standard)

START_POINT_OFFSET = 3 # start point offset (in lines)

# regex stuff
RE_TWEET_STARTER = r'"https://x.com/([^/]*)/status/([^/]*)"'    # used to find the url which marks where the author and datetime information will be
RE_DATETIME = r'datetime="([^"]*)"'                         # used to find the datetime information specifically
RE_TWEET_INDICATOR = r"tweetText"                           # used to find the start of a tweet's contents (occurs sometime after a tweet url)
RE_CLASS_START = r'class="([^"]*)"'                         # used to find the garbage html on the first line of a tweet's content
RE_SPAN_START = r"<span"                                    # used to check if a tweet contains text
RE_EMOJI_START = r"</span><img"                             # emojis appear as these elements within an existing tweet's content
RE_SPAN_END = r"</span>"                                    # used to find the end of a tweet's contents
RE_DIV = r"</div>"

# returns a dictionary with the nested keys listed above
def make_subdict() -> dict[str, str]:
    subdict = {
        KEY_CONTENT: None, 
        KEY_AUTHOR: None, 
        KEY_DATE: None
    }
    return subdict

# removes garbage from a string
# garbage consists of
#   class="... ... ... ... ..."> at the start of the string
#   </span> at the end of the string
def clean_str(string:str) -> str:
    garbage_start = re.search(RE_CLASS_START, string)
    garbage_span = re.search(RE_SPAN_END, string)
    if garbage_start:
        string = string[garbage_start.end() + 1:]
    if garbage_span:
        string = string[:garbage_span.start()]
    return string

# gets the username from a url like
# "https://x.com/<username>/status/<numbers>"
# PRECONDITION: the inputted string must be in this format
def get_username(string:str) -> str:
    return string[14:re.search(r"/status/", string).start()]

# turns a url into a post id
# "https://x.com/<username>/status/<numbers>" -> "<username><number>"
# PRECONDITION: the inputted string must be in this format
def get_postid(string:str) -> str:
    midpoint = re.search(r"/status/", string)
    return string[14:midpoint.start()].lower() + string[midpoint.end():-1] 

# gets the datetime from a datetime element
# datetime="<datetime>" -> <datetime>
# PRECONDITION: the inputted string must be in this format
def get_date(string:str) -> str:
    start = re.search(r'"', string)
    return string[start.start()+1:-1]

os.chdir("../../") # go up to the app directory

try:
    with open(f"{OUTPUT_PATH}{OUTPUT_MASTER}_MASTER.json", "r") as f:
        tweet_contents = json.load(f)
except FileNotFoundError:
    print("No existing json")

os.chdir("tools/twitter_scraper")

try:
    added = 0
    skipped = 0
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        found_starter = False  # whether data has been found for the next tweet's contents
        reading = False        # whether we are currently reading a tweet's contents
        skipping_emoji = False # whether or not the parser is currently skipping an emoji
        start_point = 0        # the line to begin reading
        curr_id = ""           # id of the current tweet we are reading
        curr_content = ""      # the current message we are reading

        for line_num, line in enumerate(f):
            starter = re.search(RE_TWEET_STARTER, line)
            if starter: # FOUND TWEET "starter", contains a link to the tweet, along with datetime
                url = line[starter.start()+1:starter.end()]
                username = get_username(url).lower()
                curr_id = get_postid(url)
                if curr_id in tweet_contents: # already exists
                    print(f"{curr_id} already exists! Skipping...")
                    skipped += 1
                else:
                    tweet_contents[curr_id] = make_subdict() # add an entry for this tweet in the dictionary
                    tweet_contents[curr_id][KEY_AUTHOR] = username
                    found_starter = True
                    added += 1
                    #i += 1 # COUNTER FOR DEBUG PURPOSES
            
            date = re.search(RE_DATETIME, line)
            if curr_id in tweet_contents and tweet_contents[curr_id][KEY_DATE] is None and date:
                tweet_contents[curr_id][KEY_DATE] = get_date(line[date.start()+1:date.end()])

            if re.search(RE_TWEET_INDICATOR, line) and found_starter: # BEGIN READ if starter information exists
                reading = True
                found_starter = False
                start_point = line_num + START_POINT_OFFSET

            if reading:
                if not skipping_emoji: # things that can only happen if parser is not currently skipping over an emoji
                    if line_num == start_point - 1 and not re.search(RE_SPAN_START, line): # if the tweet is not text, END READ immediately
                        reading = False
                        continue
                    if line_num >= start_point:
                        curr_content += clean_str(line.strip()) + " " # add message content, without the newline and leading/trailing whitespace
                else: # THE PARSER IS CURRENTLY SKIPPING OVER AN EMOJI
                    if re.search(RE_DIV, line):
                        #print(curr_content)
                        tweet_contents[curr_id][KEY_CONTENT] = curr_content # add message contents to dict entry
                        reading = False
                        curr_content = ""
                        continue
                    if re.search(RE_SPAN_START, line): 
                        start_point = line_num + 1
                        skipping_emoji = False

                if re.search(RE_EMOJI_START, line): # determine the start of an emoji, ignore all the info inside (shift start_point)
                    skipping_emoji = True
                elif re.search(RE_SPAN_END, line): # END READ
                    #print(curr_content)
                    tweet_contents[curr_id][KEY_CONTENT] = curr_content # add message contents to dict entry
                    reading = False
                    curr_content = ""
    print(f"Finished parsing! Added {added}; Skipped {skipped}; Total entries is now {len(tweet_contents.keys())}")
except FileNotFoundError:
    print("File not found")

##############################################################################
## JSON
##############################################################################
os.chdir("../../") # go up to the app directory

try:
    with open(f"{OUTPUT_PATH}{OUTPUT_MASTER}_MASTER.json", 'x') as f:
        f.write("")
    print(f"File '{OUTPUT_PATH}{OUTPUT_MASTER}_MASTER.json' created successfully.")
except FileExistsError:
    pass
    #print(f"File '{OUTPUT_PATH}{FILE_PATH[:-5]}_MASTER.json' already exists. No new file was created.")

with open(f"{OUTPUT_PATH}{OUTPUT_MASTER}_MASTER.json", "w", encoding="utf-8") as f:
    json.dump(tweet_contents, f, indent=4)
    print("Master JSON wrote successfully")

tweets_by_user = {}
for key in tweet_contents.keys():
    username = tweet_contents[key][KEY_AUTHOR]
    if username not in tweets_by_user:
        tweets_by_user[username] = {}
    tweets_by_user[username][key] = make_subdict()
    tweets_by_user[username][key] = tweet_contents[key]

for username in tweets_by_user.keys():
    DEST = f"{OUTPUT_PATH}{username}.json"
    try:
        with open(DEST, 'x') as f:
            f.write("")
        print(f"File '{DEST}' created successfully.")
    except FileExistsError:
        #print(f"File '{DEST}' already exists. No new file was created.")
        pass

    with open(DEST, "w", encoding="utf-8") as f:
        json.dump(tweets_by_user[username], f, indent=4)
        #print("JSON wrote successfully")