from tweet_fetcher import TweetFetcher
from sentiment_analyser import SentimentAnalyser
import tweepy
from datetime import datetime, timedelta

TESTING = True

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


  '''
  Do a sentiment analysis against tweets for each couple to get a compound score
  '''
  def get_couple_scores(self):
    analyser = SentimentAnalyser()

    # Get tweets
    if not TESTING:
      self.get_love_island_tweets()
      # Get formatted tweets categorised by pair
      all_tweets = self.pair_tweets
    else:
      all_tweets = get_test_string()

    couple_scores = []
    # Loop through the tweets and get a list of compound score for sentiment of each tweet
    for pair in all_tweets:
      score = []
      pair_tweets = all_tweets[pair]
      for tweet in pair_tweets:
        score.append(analyser.get_sentiment_for_text(tweet))

      # get the average score
      average_score = sum(score) / float(len(score))
      couple_scores.append({
        'pair': pair,
        'score': average_score
      })

    # sort them by their total score
    couple_scores.sort(key=lambda x: x['score'], reverse=True) 
    return couple_scores


# Use for testing so we don't ram the free API with requests
def get_test_string():
  return {"alex alexandra": ["Dr Alex won\u2019t look Alexandra in the eye he\u2019s definitely lying to her \u2060", "How in TF is someone like Alexandra letting someone like Alex worry her WTF What s happening in this world LMAOO t\u2026", "really fucks me off that someone as genuine as Alexandra and kind and GORGEOUS and SEXY can be made to feel inadequ\u2026", "I actually appreciate Alexandra s sexiness but at the same time she s not for me I wouldn t look at her and fanc\u2026", "Alexandra needs more confidence She is stunning Like that Jess who used to be on that programme abt\u2026", "Alex just isn\u2019t man enough to handle a woman like Alexandra and quite frankly it\u2019s hilarious poor chap", "alexandra is honestly unreal how does alex not fancy her", "Why can I see every vein in Alex amp Alexandra\u2019s body", "If Alex and Alexandra get saved tomorrow i\u2019ll be fuming", "Is Dr Alex dense Alexandra opens up about being unsure about how he feels she\u2019s in bed with literal open arms an\u2026"], "jack dani": ["Mood when jack and Dani made up", "charlesf amp MasDyer are theeee cutest couple they have to win \ud83d\ude48\ud83d\ude48\ud83d\ude48", "Catching up on and I\u2019m so happy MasDyer amp charlesf worked things out that I have tears in my eyes \ud83d\ude48\ud83d\ude48\ud83d\ude48\ud83d\ude48", "mateee jack and dani are just perfect for each other", "Jack and dani are just that couple you wanna meet on holiday", "hey cami babe x have you been watching this year What do you think of MasDyer and\u2026", "who will be responsible for ultimately wrecking Jack and Dani s relationship", "Also Jack and Dani flirting after he smacked her on the butt WAS EVERYTHING \ud83d\ude02\ud83d\ude02\ud83d\udc95\ud83d\udc95#myfavs", "Legit worried all day about Jack and Dani I m too invested I know it s pathetic so glad to see they re alright", "If jack and dani don\u2019t win love island they\u2019ll be losing a viewer next year"], "josh kaz": ["Funny how Josh and kaz are seen as boring because they are the only couple intelligent enough to realise there s no\u2026", "Now the Fiats are saying Josh amp Kaz are too boring to win LOOL you lot have a sickness", "Can t believe you lot bring race into everything As a woc I can honestly say the colour of their skin has absolute\u2026", "qwhite interesting how josh amp kaz are getting hate for literally doing nothing but love each other amp be happy together \ud83e\udd14\ud83e\udd14", "I m still rattled you know Smug Don t Josh amp Kaz deserve happiness What s even wrong with this public", "Josh and Kaz are boring as fuck", "Josh and Kaz win or the whole shows rigged idc", "Josh and Kaz are the best couple hands down throw Fiat 500 twitter in the bin", "I do acc think kaz and Josh could win Like they ve been loved up ever since they met \u2764", "People think Josh and Kaz are smug because of the faces they pull when other people are hurting \u2060"], "laura jack": ["New Laura was insensitive with old Laura during the lie detector test asking Jack silly questions so she could boos\u2026", "JACK AND LAURA ARE ADORABLE", "Sorry new Laura but new jack probably will ditch you when he gets out and sees his dms lol", "I literally stopped watching love island after watching new jack dumped old laura How can you say you care bout h\u2026", "I need a cuddle tonight just how Jack cuddled Laura in", "Laura sounds like she\u2019s summoning Poseidon when she cries", "Ugh new laura has known new jack 5mins why is she crying", "Opinions of tonight\u2019s ep very happy mum and dad sorted it out hating to love how sarcastic old Jack was New Laur\u2026", "Like I really like hope that like New Jack like really likes New Laura because like he\u2019s actually like so\u2026", "oh shut up new jack it\u2019s so obvious you picked new laura cause of her appearance"], "wes megan": ["Megan s talk with Wes \ud83d\ude2d no worse thing than never feeling good enough so draining", "Imagine people are actually voting for Megan amp Wes All that airtime has definitely worked on you guys Wow", "I can already see Wes heartbroken over Megan in a year if not sooner", "I wish Megan was half as concerned about what her parents thought about her career then wes\u2019s\ud83d\ude02\ud83d\ude02\ud83d\ude02", "This is how Wes will treat Megan like shit on the outside and she\u2019ll just take it because she doesn\u2019t rate herself", "Do you like Megan and Wes \ud83e\udd14", "Megan is actually so cute around Wes It\u2019s adorable", "unpopular opinion Megan amp Wes are so cute and deserve more appreciation", "I think Paul actually fancies Megan he was glued to her when she was upset and talking to Wes", "Wes gone be paying for megan s top up procedures"]}