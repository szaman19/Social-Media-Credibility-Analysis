from pymongo import MongoClient
import time

client = MongoClient()
db = client['twitter_data']
tweets = db['streamed_tweets']
newCol = db['url_tweets_test']

start = time.time()

for tweet in tweets.find({"entities.urls": {'$not': {'$size': 0}}}):
    newCol.insert_one(tweet)

end = time.time() - start

# f = open("results.txt", "w+")
# f.write("Complete! Final count for newCol is ", newCol.count(), " tweets from the base collection's", tweets.count(), "\n")
# f.write("Total time elapsed: ", end, "\n")
