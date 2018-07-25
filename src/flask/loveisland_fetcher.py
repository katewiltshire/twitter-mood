from tweet_fetcher import TweetFetcher
import tweepy

class LoveIslandFetcher(TweetFetcher):
  def _get_query(self, hashtag, quantity):
    # do some extra things here about the search terms
    islanders = [
      'jack',
      'dani',
      'laura',
      'wes',
      'megan',
      'laura',
      'alex',
      'alexandra',
      'josh',
      'kaz',

    ]
    islanders_search_string = " OR ".join(islanders)
    print('islanders_search_string', islanders_search_string)
    return tweepy.Cursor(self.api.search, q='%s %s -filter:retweets' % (hashtag, islanders_search_string), lang="en").items(quantity)