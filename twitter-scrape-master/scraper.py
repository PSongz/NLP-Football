import settings
import itertools
from utils import *
import tweepy
import dataset
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy.exc import ProgrammingError
import json

db = dataset.connect(settings.CONNECTION_STRING)
tweet_dict = load('EPL_tweet_dict','C:/Users/clement.laplace/Documents/git/NLP-Football/Data/Dictionnaries/')
search_terms=list(itertools.chain.from_iterable(tweet_dict.values()))

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                text=status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text=status.retweeted_status.text
        else:
            try:
                text=status.extended_tweet["full_text"]
            except AttributeError:
                text=status.text

        description = status.user.description
        loc = status.user.location
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(text)

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        table = db[settings.TABLE_NAME]
        try:
            table.insert(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
                vader_sent = vs['compound'],
            ))
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener,tweet_mode='extended')
stream.filter(track=search_terms, is_async=True, languages= ["en"])