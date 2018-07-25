from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyser:
  def __init__(self):
    self.analyzer = SentimentIntensityAnalyzer()