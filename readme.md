# Twitter Mood

This is a project which makes use of the twitter API and sentiment analysis to extract "interesting" data.

## Technologies Used

- [tweepy](http://www.tweepy.org/) - python library for accessing the twitter API
- [vader sentiment analysis](https://github.com/cjhutto/vaderSentimentfl) - for sentiment analysis
- [flask python microframework](http://flask.pocoo.org/) - python microframework
- [docker](https://www.docker.com/) - for running locally

## Projects

### #Loveisland

Who is going to win love island? Who cares? I do. This tracks #loveisland tweets over the last 24 hours. Breaks them into tweets about each couple, and orders them by sentiment to predict who will win.

### Mood

Track a users mood over time, based on the sentiment of their tweets.

## Installing

You will need docker on your machine. 

In the terminal run:

```
cd src && ./bowser.sh start
```

This will spin up your docker container. Navigate to localhost and you should see the index page.

## Thanks

Thanks goes to:
- Massi for the docker setup
- Chris for the #loveisland idea
