from google.appengine.ext.ndb import Model, IntegerProperty
from app.auto_twitter import client


class Tweet(Model):
    id_on_twitter = IntegerProperty(required=True)

    def retweet(self):
        return client.api['statuses/retweet'][self.id_on_twitter].post()

    @staticmethod
    def search_for_required_tweets(tags=''):
        response = client.api.search.tweets.get(q=tags)
        return tuple(Tweet(id_on_twitter=int(tweet['id_str'])) for tweet in response.data['statuses'])