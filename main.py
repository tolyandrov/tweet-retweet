from webapp2 import WSGIApplication, Route
from app.handlers import HomePage
from app.auto_twitter.handlers import AutoRetweetGiveaways, RetweetWorker, RetweetAndFollowWorker

# register routes in this list
routes = [
    Route('/', handler=HomePage, name='home'),
    Route('/twitter/auto_retweet_giveaways', handler=AutoRetweetGiveaways, name='auto_retweet_giveaways'),
    Route('/twitter/retweet_worker/<tweet_id>', handler=RetweetWorker, name='retweet_worker'),
    Route('/twitter/retweet_and_follow_worker/<tweet_id>/<account_id>', handler=RetweetAndFollowWorker,
          name='retweet_and_follow_worker')
]

app = WSGIApplication(routes, debug=True)
