# utility file to interface with twitter APIs
import tweepy

# ydlp's credentials
consumer_key = "9veoQ18y7FjaOLuK1fie27PVs"
consumer_secret = "yX40CLgdoyU05PaYVQAUFoDzyQjMCTgJEMXVNvnPEqUgct77m1"
access_token = "2692437744-raQboGN0yO5lJqVB57SFSZmwiZPvYlDp4kegAhZ"
access_token_secret = "0XlwfV581PtgVef3P7QPO3KSSlYcQdFlp71CBVlcEmjrS"

# aramonta's credentials
bearerToken = "AAAAAAAAAAAAAAAAAAAAAAkTYgEAAAAA%2BH%2FbsCYLFEiIBFtZ4sLtN81gAUE%3D08wrNvUOdkoAark3oL9OD1GkTCeoHz4gIx5slUkl7WUmV9GLNV"

# Twitter API Accessors
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=bearerToken)

# Misc Constants
MIN_RESULTS = 5
DEFAULT_USER = "JoeBiden"

def getUserName(name):
    user = api.search_users(name.value)[0]
    return user.screen_name

def getUserId(user = DEFAULT_USER):
    return client.get_user(username=user)[0].id

def getLatestTweets(user = DEFAULT_USER, n = MIN_RESULTS):
    maxResults = MIN_RESULTS if n is None or n < MIN_RESULTS else n
    return client.get_users_tweets(id=getUserId(user), exclude=["retweets"], tweet_fields=["created_at"], max_results=maxResults)
