from datetime import datetime
from dateutil import tz
import re

URL_PLACEHOLDER_TEXT = '[URL]'

# i.e. 2022-01-24 16:08:02+00:00 (UTC) -> 2022-01-28 10:19:00-08:00 (PST)
def getLocalTimestamp(timestamp):
    return timestamp.astimezone(tz.tzlocal())

# i.e. 2022-01-28 10:19:00-08:00 -> Friday January 28 2022 at 10:19 AM
def getSpeakableDatetimeFromTimestamp(timestamp):
    return datetime.strftime(timestamp, "%A %B %d %Y at %I:%M %p")

# i.e. On Friday January 28 2022 at 4:20 AM, @cooluser said: This is my tweet
def getSpeakableTweet(tweet, username):
    datetime = getSpeakableDatetimeFromTimestamp(getLocalTimestamp(tweet["created_at"]))
    text = getCleanedText(tweet["text"])
    return None if not text or text is URL_PLACEHOLDER_TEXT else F'On {datetime}, @{username} said:\n{text}'

# Joins the list of tweets into a single string of speakable-tweets
def getSpeakableTweets(tweets, username):
    speakableTweets = []
    for tweet in tweets:
        speakableTweet = getSpeakableTweet(tweet, username)
        if speakableTweet:
            speakableTweets.append(speakableTweet)
    return '<break time="2s"/>'.join(speakableTweets)

# Replaces URLs in the text with '[URL]'
def getCleanedText(text):
    return re.sub(r'http\S+', URL_PLACEHOLDER_TEXT, text)
