from google.appengine.ext.ndb import Model, IntegerProperty
from app.auto_twitter import client
from datetime import datetime, timedelta


class Tweet(Model):
    id_on_twitter = IntegerProperty(required=True)
    tweeted_by_id = IntegerProperty(required=True)

    def retweet(self):
        return client.api['statuses/retweet'][self.id_on_twitter].post()

    @staticmethod
    def search_for_required_tweets(query_string='', retweet_count=0):
        response = client.api.search.tweets.get(q=query_string, count=100)
        return tuple(Tweet(id_on_twitter=int(tweet['id_str']),
                           tweeted_by_id=int(tweet['user']['id_str'])) for tweet in response.data['statuses']
                     if tweet['retweet_count'] >= retweet_count)


class Account(Model):
    id_on_twitter = IntegerProperty(required=True)

    def follow(self):
        return client.api['friendships/create'][self.id_on_twitter].post()
