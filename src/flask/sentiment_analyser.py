from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyser:
  def __init__(self):
    self.analyzer = SentimentIntensityAnalyzer()

  '''
  Returns the sentiment for a piece of text
  '''
  def get_sentiment_for_text(self, text):
    score = self.analyzer.polarity_scores(text)

    if score:
      return score['compound']
    return 0

  '''
  Returns a sentiment score against each couple in love island
  '''
  def get_love_island_couple_scores(self, all_tweets):
    couple_scores = []
    # Loop through the tweets and get a list of compound score for sentiment of each tweet
    for pair in all_tweets:
      score = []
      pair_tweets = all_tweets[pair]
      for tweet in pair_tweets:
        score.append(self.get_sentiment_for_text(tweet))

      # get the average score
      average_score = sum(score) / float(len(score))
      couple_scores.append({
        'pair': pair,
        'score': average_score
      })

    # sort them by their total score
    couple_scores.sort(key=lambda x: x['score'], reverse=True) 
    return couple_scores

  '''
    Returns sentiment over time from tweets
  '''
  def get_sentiment_over_time(self, tweets):
    scores = {}
    data = []
    for tweet in tweets:
      date = tweet['created_at'].date()
      date_string = date.strftime('%Y/%m/%d')
      sentiment = self.get_sentiment_for_text(tweet['text'])
      if scores.get(date_string):
        scores[date_string].append(sentiment)
      else:
        scores[date_string] = [sentiment]
      data.append(sentiment)

    for score in scores:
      scores[score] = sum(scores[score]) / float(len(scores[score]))
      
    print('scores =>', scores)

    return {
      'data': data,
      'scores': scores
    }

