import json
import redis
import os
from tweet import Tweet

class TweetStore:

    # Redis Configuration
    # redis_host = "localhost"
    # redis_port = 6379
    # redis_password = ""

    #redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    #redis = redis.from_url(redis_url)

    # Tweet Configuration
    redis_key = 'tweets'
    num_tweets = 20 # Trim total tweets by num_tweets
    trim_threshold = 100

    # Variable for total tweets
    limit = 50

    # Create db connection with Redis Configurations
    def __init__(self):
        # self.db = r = redis.Redis(
        #     host=self.redis_host,
        #     port=self.redis_port,
        #     password=self.redis_password
        # )
        self.redis = None
        redis_url = os.getenv(self.REDIS_URL, 'redis://localhost:6379')
        self.redis = redis.from_url(redis_url)

        self.trim_count = 0

    # Method to extract last X about of tweets 
    def tweets(self, limit=limit):
        tweets = []

        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets.append(Tweet(tweet_obj))

        return tweets
    
    def tweets1(self, limit=limit):
        tweets1 = []

        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets1.append(tweet_obj)

        return tweets1
    
    # Receive parameter data: Tweet object (tweet_item)
    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data)) # push to the head of the list
        self.trim_count += 1 # increment trim count

        # Periodically trim the list so it doesn't grow too large.
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets) # keeps recent tweets and discards oldest tweets (total - num_tweets)
            self.trim_count = 0
