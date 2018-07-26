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

## Limitations

Because I am using the free tier of the twitter API, I can't blast the API with queries. For the mood grapher, I've limited my search to the past 100 tweets and then taken an average sentiment per day. This might be effective for someone who doesn't tweet often or a less popular hashtag, but is less effective for users/hashtags with 1,000s of tweets a day - as 100 tweets might have been generated within a couple of hours.

Because hashtags tend to have way more tweets attached to them than users, we filter by twitter's parameter `result_type=popular` in order to get fewer results.

I decided to use the vader sentiment analysis package for python rather than an API, because I couldn't find a good, free sentiment analysis API.

## Thanks

Thanks goes to:
- Massi for the docker setup
- Chris for the #loveisland idea
