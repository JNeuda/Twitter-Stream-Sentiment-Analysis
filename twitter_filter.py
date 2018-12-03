import tweepy
import datetime
from tweet_store import TweetStore
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Import json file
file_path = 'config/api.json'

# Access json file
with open(file_path) as f:
    twitter_api = json.loads(f.read())

# Twitter API Keys in json file
consumer_key = twitter_api['consumer_key']
consumer_secret = twitter_api['consumer_secret']
access_token = twitter_api['access_token']
access_token_secret = twitter_api['access_token_secret']

# Authentication for tweepy API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create new API object
api = tweepy.API(auth)

# Create new instance
store = TweetStore()

#Create subclass called StreamListener and modify the methods on_status and on_error
class StreamListener(tweepy.StreamListener):

    # Information for each tweet
    def on_status(self, status):

        if ('RT @' not in status.text): #if not a retweet, run vaderSentiment on tweet and create tweet_item and extract certain properties from status)
            results = analyzer.polarity_scores(status.text)
            compound = results["compound"]
            pos = results["pos"]
            neu = results["neu"]
            neg = results["neg"]

            tweet_item = {
                'id_str': status.id_str,
                'text': status.text,
                'compound_score': compound,
                'pos_score': pos,
                'neu_score': neu,
                'neg_score': neg,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                'received_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'language': status.user.lang
            }

            # Storing data in redis
            store.push(tweet_item)
            print("Pushed to redis:", tweet_item)

    #Used for when we are being rate limited (Dependent on Twitter API). 
    def on_error(self, status_code):
        if status_code == 420:
            return False

#Create an instance of our Streamlistener Class
stream_listener = StreamListener()
#Pass authentication creditionals and our stream_listener
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

#Filter passing on a list of words/usernames 
stream.filter(track=["@BBC", "@CBS", "@CNN", "@FoxNews", "@nytimes"])

#use this to follow target users and their tweets
#stream.filter(follow=["@BBC", "@CBS", "@CNN", "@FoxNews", "@nytimes"])

#We are using vaderSentiment Analysis to see what people are saying about these key words
