import tweepy
import re
import string
import config
import utils
import random

class TweetFetcher:
  def __init__(self):
    self._setup_auth()


  '''
  Setup authentication for twitter API
  '''
  def _setup_auth(self):
    keys = config.twitter_keys()
    auth = tweepy.OAuthHandler(keys['api_key'], keys['api_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    self.api = tweepy.API(auth, wait_on_rate_limit=True)


  '''
  Returns all tweets for a given twitter username
  '''
  def get_tweets_for_user(self, twitter_user, quantity=100):
    tweets = self.api.user_timeline(
        screen_name=twitter_user,
        count=quantity
    )
    return self._tidy_tweets(tweets)
    

  '''
  Returns all tweets for a given hashtag
  '''
  def get_tweets_for_hashtag(self, hashtag, quantity=100):
    if hashtag[0] != '#':
      hashtag = '#%s' % hashtag
    tweets = self._get_query(hashtag, quantity)
    return self._tidy_tweets(tweets)
    

  '''
  Tidies list of tweets and returns list of just tweet text
  '''
  def _tidy_tweets(self, tweets):
    if not tweets:
      return []

    tweets_list = []
    for tweet in tweets:
      try:
        tweets_list.append(utils.strip_all_entities(tweet.text))
      except AttributeError:
        tweets_list.append(utils.strip_all_entities(tweet))

    return tweets_list


  '''
  Returns generic query for twitter, removes retweets and links
  '''
  def _get_query(self, hashtag, quantity):
    return tweepy.Cursor(self.api.search, q='%s -filter:retweets -filter:links' % hashtag, lang="en").items(quantity)


  '''
  Returns a random hashtag or username
  '''
  def get_random_search(self):
    hash_tags = ['apple', 'microsoft', 'uber', 'starbucks',]
    user_names = ['katyperry', 'barackobama', 'justinbieber', 'cristiano', 'therealdonald', 'kimkardashian', 'britneyspears', 'billgates', 'oprah',]

    hash_tag_searches = [{
      'type': 'hash_tag',
      'param': tag} 
      for tag in hash_tags
      ]
    user_name_searches = [{
      'type': 'user_name',
      'param': tag} 
      for tag in user_names
      ]

    return random.choice(hash_tag_searches + user_name_searches)
