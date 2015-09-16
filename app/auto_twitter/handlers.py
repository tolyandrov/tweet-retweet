from google.appengine.api import taskqueue
from webapp2 import RequestHandler

from datetime import datetime, timedelta

from app.auto_twitter import client
from app.auto_twitter.models import Tweet, Account


class AutoRetweetGiveaways(RequestHandler):
    def get(self):
        try:
            # TODO: Still need some optimisation to search right tweets
            tweets_to_retweet = Tweet.search_for_required_tweets('%23giveaway+-filter:links', 10)
            now = datetime.now()
            retweet_in = 0
            for tweet in tweets_to_retweet[-15:]:  # as we can't add more that 15 tasks in default queue
                # TODO: Check if we need to follow account that tweeted
                also_follow = False
                tweet_to_db = tweet.put()
                if also_follow:
                    account_to_db = Account(id_on_twitter=tweet.tweeted_by_id).put()
                    taskqueue.add(url='/twitter/retweet_and_follow_worker/'+str(tweet_to_db.id()) + '/' +
                                  str(account_to_db.id()),
                                  eta=now+timedelta(minutes=retweet_in))
                else:
                    taskqueue.add(url='/twitter/retweet_worker/'+str(tweet_to_db.id()),
                                  eta=now+timedelta(minutes=retweet_in))
                retweet_in += 1
            self.response.out.write('Fifteen tweets successfully scheduled to be retweeted in next fifteen minutes.')
        except Exception, msg:
            self.response.out.write(msg)


class RetweetWorker(RequestHandler):
    def post(self, tweet_id=None):
        try:
            if tweet_id:
                tweet = Tweet.get_by_id(int(tweet_id))
                tweet.retweet()
                tweet.delete()
            self.response.write('Retweeted!')
        except Exception, msg:
            self.response.write(msg)


# Doing retweet and follow as one task to save space in task queue
class RetweetAndFollowWorker(RequestHandler):
    def post(self, tweet_id=None, account_id=None):
        try:
            if tweet_id and account_id:
                tweet = Tweet.get_by_id(int(tweet_id))
                tweet.retweet()
                tweet.delete()
                account = Account.get_by_id(int(account_id))
                account.follow()
                account.delete()
            self.response.write('Retweeted and Followed!')
        except Exception, msg:
            self.response.write(msg)
