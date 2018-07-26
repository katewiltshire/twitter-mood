# Twitter Mood

This is a project which makes use of the twitter API and sentiment analysis to extract "interesting" data.

## Technologies Used

- [tweepy](http://www.tweepy.org/) - python library for accessing the twitter API
- [vader sentiment analysis](https://github.com/cjhutto/vaderSentimentfl) - for sentiment analysis
- [flask](http://flask.pocoo.org/) - the python microframework
- [docker](https://www.docker.com/) - for running the project locally
- [chartjs](https://www.chartjs.org/) - for simple javascript graphs

## Projects

### #Loveisland

Who is going to win love island? Who cares? I do. This tracks #loveisland tweets over the last 24 hours. Breaks them into tweets about each couple, and orders them by sentiment to predict who will win.

### Mood Grapher

Creates a graph, based on the sentiment for the past 100 tweets from, hashtag, user or random choice.

## Installing

You will need docker on your machine. 

In the terminal run:

```
cd src && ./bowser.sh start
```

This will spin up your docker container. Navigate to localhost and you should see the index page.

This repository does not contain any twitter API keys. You will need to create a `config.py` file in the /flask directory, with the following function, filling in your own API keys. These can be found in the [twitter apps hub](https://apps.twitter.com/).

```
def twitter_keys():
  return {
    'api_key': <your_api_key>,
    'api_secret': <your_api_secret>,
    'access_token': <your_access_token>,
    'access_token_secret': <your_access_token_secret>
  }
```

## Thanks

Thanks goes to:
- Massi for the docker setup
- Chris for the #loveisland idea
