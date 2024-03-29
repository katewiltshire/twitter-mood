from flask import Flask, render_template, request
from tweet_fetcher import TweetFetcher
from sentiment_analyser import SentimentAnalyser
from loveisland_fetcher import LoveIslandFetcher

TESTING = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/mood', methods = ['GET', 'POST'])
def analyse_tweets():
    sentiment_analyser = SentimentAnalyser()

    user_name = request.form.get('user_name')
    hash_tag = request.form.get('hash_tag')
    form_type = request.form.get('type')

    if not user_name and not hash_tag and not form_type:
        return render_template('mood.html', type=False)

    tweets = []
    scores = []
    query = {
        'type': form_type
    }

    if not TESTING:

        tweet_fetcher = TweetFetcher()

        if form_type == 'user_name' and user_name:
            tweets = tweet_fetcher.get_tweets_for_user(user_name)
            query['param'] = user_name
        elif form_type == 'hash_tag' and hash_tag:
            tweets = tweet_fetcher.get_tweets_for_hashtag(hash_tag)
            query['param'] =  hash_tag
        elif form_type == 'random':
            query = tweet_fetcher.get_random_search()
            if query['type'] is 'hash_tag':
                tweets = tweet_fetcher.get_tweets_for_hashtag(query['param'])
            else:
                tweets = tweet_fetcher.get_tweets_for_user(query['param'])

        if tweets:
            scores = sentiment_analyser.get_sentiment_over_time(tweets)
    
    else:
        scores = TEST_SCORES
        query['type'] = 'user_name'
        query['param'] = 'katezerooo'

    return render_template('mood.html', scores=scores, type=form_type, query=query)


@app.route('/loveisland')
def love_island():
    sentiment_analyser = SentimentAnalyser()
    tweet_fetcher = LoveIslandFetcher()
    couple_scores = []

    if not TESTING:
        love_island_tweets = tweet_fetcher.get_love_island_tweets()
        print("love island tweets =>", love_island_tweets)
    else:
        love_island_tweets = TEST_TWEETS

    if love_island_tweets and len(love_island_tweets) > 0:
        couple_scores = sentiment_analyser.get_love_island_couple_scores(love_island_tweets)

    return render_template('loveisland.html', couple_scores=couple_scores)

# Use for testing so we don't ram the free API with requests

TEST_TWEETS = {"alex alexandra": ["Dr Alex won\u2019t look Alexandra in the eye he\u2019s definitely lying to her \u2060", "How in TF is someone like Alexandra letting someone like Alex worry her WTF What s happening in this world LMAOO t\u2026", "really fucks me off that someone as genuine as Alexandra and kind and GORGEOUS and SEXY can be made to feel inadequ\u2026", "I actually appreciate Alexandra s sexiness but at the same time she s not for me I wouldn t look at her and fanc\u2026", "Alexandra needs more confidence She is stunning Like that Jess who used to be on that programme abt\u2026", "Alex just isn\u2019t man enough to handle a woman like Alexandra and quite frankly it\u2019s hilarious poor chap", "alexandra is honestly unreal how does alex not fancy her", "Why can I see every vein in Alex amp Alexandra\u2019s body", "If Alex and Alexandra get saved tomorrow i\u2019ll be fuming", "Is Dr Alex dense Alexandra opens up about being unsure about how he feels she\u2019s in bed with literal open arms an\u2026"], "jack dani": ["Mood when jack and Dani made up", "charlesf amp MasDyer are theeee cutest couple they have to win \ud83d\ude48\ud83d\ude48\ud83d\ude48", "Catching up on and I\u2019m so happy MasDyer amp charlesf worked things out that I have tears in my eyes \ud83d\ude48\ud83d\ude48\ud83d\ude48\ud83d\ude48", "mateee jack and dani are just perfect for each other", "Jack and dani are just that couple you wanna meet on holiday", "hey cami babe x have you been watching this year What do you think of MasDyer and\u2026", "who will be responsible for ultimately wrecking Jack and Dani s relationship", "Also Jack and Dani flirting after he smacked her on the butt WAS EVERYTHING \ud83d\ude02\ud83d\ude02\ud83d\udc95\ud83d\udc95#myfavs", "Legit worried all day about Jack and Dani I m too invested I know it s pathetic so glad to see they re alright", "If jack and dani don\u2019t win love island they\u2019ll be losing a viewer next year"], "josh kaz": ["Funny how Josh and kaz are seen as boring because they are the only couple intelligent enough to realise there s no\u2026", "Now the Fiats are saying Josh amp Kaz are too boring to win LOOL you lot have a sickness", "Can t believe you lot bring race into everything As a woc I can honestly say the colour of their skin has absolute\u2026", "qwhite interesting how josh amp kaz are getting hate for literally doing nothing but love each other amp be happy together \ud83e\udd14\ud83e\udd14", "I m still rattled you know Smug Don t Josh amp Kaz deserve happiness What s even wrong with this public", "Josh and Kaz are boring as fuck", "Josh and Kaz win or the whole shows rigged idc", "Josh and Kaz are the best couple hands down throw Fiat 500 twitter in the bin", "I do acc think kaz and Josh could win Like they ve been loved up ever since they met \u2764", "People think Josh and Kaz are smug because of the faces they pull when other people are hurting \u2060"], "laura jack": ["New Laura was insensitive with old Laura during the lie detector test asking Jack silly questions so she could boos\u2026", "JACK AND LAURA ARE ADORABLE", "Sorry new Laura but new jack probably will ditch you when he gets out and sees his dms lol", "I literally stopped watching love island after watching new jack dumped old laura How can you say you care bout h\u2026", "I need a cuddle tonight just how Jack cuddled Laura in", "Laura sounds like she\u2019s summoning Poseidon when she cries", "Ugh new laura has known new jack 5mins why is she crying", "Opinions of tonight\u2019s ep very happy mum and dad sorted it out hating to love how sarcastic old Jack was New Laur\u2026", "Like I really like hope that like New Jack like really likes New Laura because like he\u2019s actually like so\u2026", "oh shut up new jack it\u2019s so obvious you picked new laura cause of her appearance"], "wes megan": ["Megan s talk with Wes \ud83d\ude2d no worse thing than never feeling good enough so draining", "Imagine people are actually voting for Megan amp Wes All that airtime has definitely worked on you guys Wow", "I can already see Wes heartbroken over Megan in a year if not sooner", "I wish Megan was half as concerned about what her parents thought about her career then wes\u2019s\ud83d\ude02\ud83d\ude02\ud83d\ude02", "This is how Wes will treat Megan like shit on the outside and she\u2019ll just take it because she doesn\u2019t rate herself", "Do you like Megan and Wes \ud83e\udd14", "Megan is actually so cute around Wes It\u2019s adorable", "unpopular opinion Megan amp Wes are so cute and deserve more appreciation", "I think Paul actually fancies Megan he was glued to her when she was upset and talking to Wes", "Wes gone be paying for megan s top up procedures"]}

TEST_SCORES = [0.0, 0.0, 0.0, 0.3612, 0.0, 0.0, 0.4215, 0.4404, -0.3412, 0.3612, 0.0, 0.0, 0.4767, 0.4404, 0.4404, 0.0, 0.5267, -0.7003, 0.8807, 0.4767, 0.6249, 0.0, 0.0258, 0.872, 0.0, 0.0, 0.0, 0.0258, 0.6369, 0.0, 0.4939, 0.0, 0.0, 0.5859, 0.7964, 0.5267, 0.3818, 0.5267, 0.0, 0.0, 0.0, -0.2023, 0.3612, 0.3612, 0.0, 0.4767, 0.0, 0.836, 0.0, 0.0, 0.1027, 0.4019, 0.836, -0.4404, 0.3182, 0.0, 0.6369, 0.3612, 0.4767, 0.7906, 0.3612, 0.0, 0.0, 0.0, -0.3412, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4767, 0.0, 0.0, 0.0, 0.0, 0.3612, 0.0, 0.0, 0.4404, 0.0, 0.4019, 0.25, 0.3612, 0.25, 0.5267, 0.4588, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3336, 0.0]