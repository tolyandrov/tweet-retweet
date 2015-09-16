from webapp2 import WSGIApplication, Route
from app.handlers import HomePage
from app.auto_twitter.handlers import AutoRetweetGiveaways, RetweetWorker

# register routes in this list
routes = [
    Route('/', handler=HomePage, name='home'),
    Route('/twitter/auto_retweet_giveaways', handler=AutoRetweetGiveaways, name='auto_retweet_giveaways'),
    Route('/twitter/retweet_worker/<tweet_id>', handler=RetweetWorker, name='retweet_worker')
]

app = WSGIApplication(routes, debug=True)
