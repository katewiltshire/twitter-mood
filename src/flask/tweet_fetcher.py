import tweepy
import re
import string
import config

class TweetFetcher:
  def __init__(self):
    self._setup_auth()

  def _setup_auth(self):
    keys = config.twitter_keys()
    auth = tweepy.OAuthHandler(keys['api_key'], keys['api_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    self.api = tweepy.API(auth)

  def get_tweets_for_user(self, twitter_user, quantity=100):
    tweets = self.api.user_timeline(
        screen_name=twitter_user,
        count=quantity
    )
    tweets_list = []
    for tweet in tweets:
      tweets_list.append(strip_all_entities(tweet.text))
    return tweets

  def get_tweets_for_hashtag(self, hashtag, quantity=100):
    if hashtag[0] != '#':
      hashtag = '#%s' % hashtag

    tweets = self._get_query(hashtag, quantity)

    tweets_list = []
    for tweet in tweets:
      tweets_list.append(strip_all_entities(tweet.text))
    return tweets_list

  def _get_query(self, hashtag, quantity):
    return tweepy.Cursor(self.api.search, q='%s -filter:retweets -filter:links' % hashtag, lang="en").items(quantity)


'''
Strips links from string
'''
def strip_links_from_text(text):
  link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
  links         = re.findall(link_regex, text)
  for link in links:
      text = text.replace(link[0], ', ')    
  return text

def strip_all_entities(text):
    text = strip_links_from_text(text)

    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)
