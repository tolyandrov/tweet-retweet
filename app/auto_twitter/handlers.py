from google.appengine.api import taskqueue
from webapp2 import RequestHandler

from datetime import datetime, timedelta

from app.auto_twitter.models import Tweet


class AutoRetweetGiveaways(RequestHandler):
    def get(self):
        try:
            # TODO: Optimize search algorithm to retweet effectively
            tweets_to_retweet = Tweet.search_for_required_tweets('%23giveaway')
            now = datetime.now()
            retweet_in = 0
            for tweet in tweets_to_retweet[-15:]:  # as we can't add more that 15 tasks in default queue
                tweet_to_db = tweet.put()
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
