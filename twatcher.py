from flask import Flask, render_template, jsonify
from tweet_store import TweetStore
import json
import pandas as pd

app = Flask(__name__)
store = TweetStore()


@app.route('/')
def index():
    tweets = store.tweets()
    return render_template('index.html', tweets=tweets)

@app.route('/tweets')
def tweets():

    results_list = []
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []
    number_list = []
    tweet_list = []
    users = []

    counter = 0

    for tweet in TweetStore().tweets1():

        compound_list.append(tweet["compound_score"])
        positive_list.append(tweet["pos_score"])
        negative_list.append(tweet["neg_score"])
        neutral_list.append(tweet["neu_score"])
        tweet_list.append(tweet["text"])

        counter += 1

        number_list.append(counter)

        if "@BBC" in tweet["text"]:
            users.append("@BBC") 
        elif "@CBS" in tweet["text"]:
            users.append("@CBS")
        elif "@CNN" in tweet["text"]:
            users.append("@CNN") 
        elif "@FoxNews" in tweet["text"]:
            users.append("@FoxNews") 
        elif "@nytimes" in tweet["text"]:
            users.append("@nytimes")
        else:
            users.append("N/A")

    sent ={
            "User": users,
            "Compound": compound_list,
            "Positive": positive_list,
            "Neutral": negative_list,
            "Negative": neutral_list,
            "Tweets_Ago": number_list,#len(compound_list),
            "Tweets": tweet_list
            }

    results_list.append(sent)

    return jsonify(results_list[0])

if __name__ == '__main__':
    app.run(debug=True)
