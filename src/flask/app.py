from flask import Flask, render_template, request
from tweet_fetcher import TweetFetcher
from loveisland_fetcher import LoveIslandFetcher
from sentiment_analyser import SentimentAnalyser

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
    
@app.route('/analyse', methods=['POST'])
def analyse_tweets():
    twitter_user = request.form.get('twitter_username')
    hashtag = request.form.get('twitter_hashtag')

    tweet_fetcher = TweetFetcher()
    if twitter_user:
        tweets = tweet_fetcher.get_tweets_for_user(twitter_user)
    elif hashtag:
        tweets = tweet_fetcher.get_tweets_for_hashtag(hashtag)

    return render_template('results.html', analysis=[])


@app.route('/loveisland')
def love_island():
    tweet_fetcher = LoveIslandFetcher()
    tweets = tweet_fetcher.get_tweets_for_hashtag('loveisland')

    return render_template('loveisland.html', analysis=tweets)