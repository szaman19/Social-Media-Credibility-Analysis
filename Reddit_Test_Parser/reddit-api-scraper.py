#! usr/bin/python3

# group06 IP - 128.226.28.226

import hashlib
import json
import pymongo
import requests as r
import time

CLIENT_ID = 'FYQkQXZ5oDgBnA'
CLIENT_SECRET = 'zVeoKmLP1Ovz1grhnbjK0XWd4pA'
REDIRECT_URI = 'http://localhost:8080'

USERNAME = 'cs480n'
PASSWORD = 'redditcrawler'

SLEEP_TIME = 250

# checks for update to list of subreddits
def check_update(file_hash):
    f = open("subs_to_search.txt", 'rb')
    hashed_file = hashlib.md5(f.read()).hexdigest()
    f.close()
    return hashed_file == file_hash

# updates list of subreddits in case of hash discrepancy
def update_subs_list(subs):
    f = open("subs_to_search.txt", "r")

    for subreddit in f:
        if(not (subreddit in subs.keys())):
            subs[subreddit.rstrip()] = 0

    f.close()
    return subs

def get_post(subreddit, post_id):
    post = r.get(f'http://www.reddit.com/r/{subreddit}/{post_id}/.json')
    post_json = post.json()

    ret_dict = {}
    ret_dict['post'] = post_json[0]
    ret_dict['comments'] = post_json[1]
    return ret_dict


def crawl_sub(subreddit, submissions):
    
    
    return

def main():

    
    f.open("subs_to_search.txt", "rb")
    file_hash = hashlib.md5(f.read()).hexdigest()
    f.close()

    # instantiate list of subreddits to search
    subs = {}
    subs = update_subs_list(subs)
    print(subs)

    # connect to Mongo DB
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    reddit_db = myclient["reddit_data"]
    collection = reddit_db["searched_posts"]

    # collection loop
    while(True):

        if (not check_update(file_hash)):
            subs = update_subs_list(subs)

        for subreddit in subs:
            subs[subreddit] = crawl_sub(subreddit)

        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()

