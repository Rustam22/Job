import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

pd.options.display.max_columns = 50
pd.options.display.max_rows= 50
pd.options.display.width= 120


consumer_key = "1igVGJGi5hiIw8kS9tmY2c9Vg" # Use your own key. To get a key https://apps.twitter.com/
consumer_secret = "EvZksD2bMZxTgF41ydIwkDN5dTwTf67ztxltDbzgg8KXFo5PxD"

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

api = tweepy.API(auth)

results = api.search(q="IPython")
print results
print len(results), "\n\n"


def print_tweet(tweet):
    print "@%s - %s (%s)" % (tweet.user.screen_name, tweet.user.name, tweet.created_at)
    print tweet.text

tweet=results[1]
print_tweet(tweet)
print "\n\n"




tweet=results[2]

for param in dir(tweet):
    if not param.startswith("_"):
        print "%s : %s" % (param, eval("tweet." + param))
print "\n\n"





user=tweet.author

for param in dir(user):
    if not param.startswith("_"):
        print "%s : %s" % (param, eval("user." + param))
print "\n\n"



"Using Cursor for Pagination"
"For data mining you will be dealing with a large amount of results. Cursor is a simple way to handle interation and results pages."
results = []
for tweet in tweepy.Cursor(api.search, q="IPython").items(100):
    results.append(tweet)

print len(results), "\n\n"





"Store Results in a Data Frame"
def process_results(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])

    # Processing Tweet Data

    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
    data_set["source"] = [tweet.source for tweet in results]

    # Processing User Data
    data_set["user_id"] = [tweet.author.id for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_name"] = [tweet.author.name for tweet in results]
    data_set["user_created_at"] = [tweet.author.created_at for tweet in results]
    data_set["user_description"] = [tweet.author.description for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set["user_friends_count"] = [tweet.author.friends_count for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]

    return data_set

data_set = process_results(results)

"Looking at the Data"
print data_set.head(5), "\n\n"
print data_set.tail(5), "\n\n"





"Visualizing Results"
sources = data_set["source"].value_counts()[:5][::-1]
plt.figure(figsize=(11.5, 4))
plt.barh(xrange(len(sources)), sources.values)
plt.yticks(np.arange(len(sources)) + 0.4, sources.index)
plt.show()