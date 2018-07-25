from flask import Flask, render_template, request
from tweet_fetcher import TweetFetcher
from sentiment_analyser import SentimentAnalyser
from loveisland_fetcher import LoveIslandFetcher

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
    
@app.route('/mood/<user_name>')
def analyse_tweets(user_name):
    scores = []

    tweet_fetcher = TweetFetcher()
    if user_name:
        tweets = tweet_fetcher.get_tweets_for_user(user_name)

        analyser = SentimentAnalyser()
        for tweet in tweets:
            score = analyser.get_sentiment_for_text(tweet)
            scores.append(score)
    
    print('scores', scores)
    
    return render_template('mood.html', scores=scores)


@app.route('/loveisland')
def love_island():
    tweet_fetcher = LoveIslandFetcher()
    couple_scores = tweet_fetcher.get_couple_scores()



    return render_template('loveisland.html', couple_scores=couple_scores)