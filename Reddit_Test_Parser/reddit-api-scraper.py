#! usr/bin/python3

# group06 IP - 128.226.28.226

import hashlib
import json
import pymongo
import requests as r
import requests.auth
import time

CLIENT_ID = 'FYQkQXZ5oDgBnA'
CLIENT_SECRET = 'zVeoKmLP1Ovz1grhnbjK0XWd4pA'
REDIRECT_URI = 'http://localhost:8080'

USERNAME = 'cs480n'
PASSWORD = 'redditcrawler'

SLEEP_TIME = 250

# retrieves OAuth2 token from Reddit for our application
def get_token():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    params = {}
    params['grant_type'] = 'password'
    params['username'] = USERNAME
    params['password'] = PASSWORD
    headers = {'User-Agent': 'cs480n-crawler by cs480n'}
    
    response = r.post("http://www.reddit.com/api/v1/access_token", auth=client_auth, data=params, headers=headers)

    return response.json()

# uses retrieved token so we can begin crawling
def use_token(response_json):
    headers = { 'Authorization': f"{response.json['token_type']} {response_json['access_token']}",
                "User-Agent": "cs480n-crawler by cs480n"}
    response = r.get("http://oauth.reddit.com/api/v1/me", headers=headers)
    return response.json()

# checks for update to list of subreddits
def check_update(file_hash):
    f = open("subs_to_search.txt", 'rb')
    hashed_file = hashlib.md5(f.read()).hexdigest()
    f.close()
    return hashed_file == file_hash


# returns list of subreddits queued to crawl
def update_subs_list(subs):
    f = open("subs_to_search.txt", "r")

    for subreddit in f:
        if(not (subreddit in subs.keys())):
            subs[subreddit.rstrip()] = 0

    f.close()
    return subs


# returns dictionary of a post's JSON return dictionary
def get_post(subreddit, post_id):
    post = r.get(f'http://www.reddit.com/r/{subreddit}/{post_id}/.json')
    post_json = post.json()

    ret_dict = {}
    ret_dict['post'] = post_json[0]
    ret_dict['comments'] = post_json[1]
    return ret_dict

# crawls newest posts on given subreddit until most recent post of last search (or limit reached)
def crawl_sub(subreddit, most_recent_id):
    subreddit_new = r.get(f'http://www.reddit.com/r/{subreddit}/new/.json?limit=1000')
    sub_new_json = subreddit_new.json()

    posts = sub_new_json['data']['children']
    post_num = 0    
    while post_num in posts:
        curr_post = posts[post_num]['data']
        if (curr_post['id'] == most_recent_id):
            break
        curr_post_data = get_post(subreddit, curr_post['id'])
        collection.insert_one(curr_post_data)
    
        post_num += 1

    new_most_recent_id = posts[0]['data']['id']

    return new_most_recent_id


def main():

    # authorize application and recieve token from oauth2
    get_token_response = get_token()
    use_token_response = use_token(get_token_response)  

    # instantiate MD5 checksum for list of subreddits
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

        # checks if list of subreddits to crawl has changed
        if (not check_update(file_hash)):
            subs = update_subs_list(subs)

        # crawls each subreddit on list
        for subreddit in subs:
            subs[subreddit] = crawl_sub(subreddit, subs[subreddit])

        # waits to put some throttling on mongo storage rate
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()

