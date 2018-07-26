from tweet_fetcher import TweetFetcher
from sentiment_analyser import SentimentAnalyser
import tweepy
from datetime import datetime, timedelta


class LoveIslandFetcher(TweetFetcher):

  '''
  Returns all tweets in the last 24 hours with the hashtag love island
  '''
  def get_love_island_tweets(self, hashtag='#loveisland', quantity=100):

    # get 24 hours ago
    now = datetime.today().now()
    yesterday = now-timedelta(days=1)
    now = now.strftime("%Y-%m-%d")
    yesterday = yesterday.strftime("%Y-%m-%d")

    pairs = self._get_pairs()

    pair_tweets = {}
    for pair in pairs:
      exclude_string = self._get_exclude_string(pair)
      tweets = tweepy.Cursor(self.api.search, q='%s %s -filter:retweets %s' % (hashtag, pair, exclude_string), since=yesterday, until=now, lang="en").items(quantity)
      if not tweets:
        pair_tweets[pair] = []
      else:
        tidied_tweets = self._tidy_tweets(tweets)
        pair_tweets[pair] = tidied_tweets

    self.pair_tweets = pair_tweets

  '''
  Returns list of pairs
  '''
  def _get_pairs(self):
    return [
      'jack dani',
      'laura jack',
      'wes megan',
      'laura paul',
      'alex alexandra',
      'josh kaz',
    ]
  
  '''
  Returns a string of all people (appended by '-') excluding the pair we are searching for
  '''
  def _get_exclude_string(self, pair):
    # get a string for the pair, e.g. "jack dani"
    this_pair = pair.split()
    # get a string of all pairs, e.g. "jack dani laura jack wes megan"
    all_pairs = " ".join(self._get_pairs()).split()
    # filter out from this list the names in this_pair, e.g. "laura jack wes megan"
    pairs_without_this_pair  = [name for name in all_pairs if name not in this_pair]
    # append a '-' before each name, e.g. "-laura -jack -wes -megan"
    search_string = "-%s" % (" -".join(pairs_without_this_pair))

    return search_string
