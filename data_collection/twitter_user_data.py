import pymongo 
import Twitter_Request
import requests as r
import json
import Twitter_Token_Utils
import hashlib
import time

def check_update(file_hash):
	f = open("user_ids.txt",'rb')
	hashed_file = hashlib.md5(f.read()).hexdigest()
	f.close()
	return hashed_file == file_hash

def update_search_terms(search_terms):

	f = open("user_ids.txt","r")

	for term in f:
		if(not (term in search_terms.keys())):
			search_terms[term.rstrip()] = 1

	f.close()
	return search_terms

def get_tweets(params, term, since_id, collection):
	params['user_id'] = term
	params['since_id'] =  since_id
	TR = Twitter_Request.Request(params, user=True).get_request(custom_query = True)

	TR = TR.prepare()
	session = r.Session()

	resp = session.send(TR)


	print(resp.text)
	tweets = json.loads(resp.text)

	ret_val = since_id

	try:
		
		for each in tweets:
			print(each['created_at'], each['id'])
			collection.insert_one(each)
		ret_val = tweets['search_metadata']['max_id']
	except Exception as e:
		print(e)


	session.close()
	time.sleep(10)
	return ret_val
	# return tweets['search_metadata']['max_id']

	# myclient = pymongo.MongoClient("mongodb://loc")
def main():
	tokens = Twitter_Token_Utils.get_tokens()
	params = {}
	params["oauth_consumer_key"] = tokens['API']
	params["oauth_access_key"] = tokens ['ACCESS']
	params["oauth_consumer_key_secret"] = tokens["API_SECRET"]
	params["oauth_access_key_secret"] = tokens ["ACCESS_SECRET"]
	params['url'] = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	params['request_type'] = "GET"
	params['count'] = 200
	# params['result_type'] = "recent"


	f = open("user_ids.txt",'rb')
	file_hash = hashlib.md5(f.read()).hexdigest()
	f.close()

	search_terms = {}
	search_terms = update_search_terms(search_terms)
	print(search_terms)

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	twitter_db = myclient["twitter_data"]
	collection = twitter_db["user_tweets"]

	# get_tweets(params, "Donald Trump",search_terms['Donald Trump'], collection)

	while(True):
		if (not check_update(file_hash)):
			search_terms = update_search_terms(search_terms)
		for each in search_terms:
			search_terms[each] = get_tweets(params, each, search_terms[each],collection)
			
main()






