from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyser:
  def __init__(self):
    self.analyzer = SentimentIntensityAnalyzer()

  def get_sentiment_for_text(self, text):
    score = self.analyzer.polarity_scores(text)

    if score:
      return score['compound']
    return 0