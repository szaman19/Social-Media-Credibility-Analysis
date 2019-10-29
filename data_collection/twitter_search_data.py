import pymongo 
import Twitter_Request
import requests as r
import json
import Twitter_Token_Utils
import hashlib
import time

def check_update(file_hash):
	f = open("search_terms.txt",'rb')
	hashed_file = hashlib.md5(f.read()).hexdigest()
	f.close()
	return hashed_file == file_hash

def update_search_terms(search_terms):

	f = open("search_terms.txt","r")

	for term in f:
		if(not (term in search_terms.keys())):
			search_terms[term.rstrip()] = 0

	f.close()
	return search_terms

def get_tweets(params, term, since_id, collection):
	params['q'] = term
	params['since_id'] =  since_id
	TR = Twitter_Request.Request(params, search=True).get_request(custom_query = True)

	TR = TR.prepare()
	session = r.Session()

	resp = session.send(TR)
	tweets = json.loads(resp.text)

	for each in tweets['statuses']:
		print(each['created_at'], each['id'])
		collection.insert_one(each)

	session.close()

	return tweets['search_metadata']['max_id']

	# myclient = pymongo.MongoClient("mongodb://loc")
def main():
	tokens = Twitter_Token_Utils.get_tokens()
	params = {}
	params["oauth_consumer_key"] = tokens['API']
	params["oauth_access_key"] = tokens ['ACCESS']
	params["oauth_consumer_key_secret"] = tokens["API_SECRET"]
	params["oauth_access_key_secret"] = tokens ["ACCESS_SECRET"]
	params['url'] = "https://api.twitter.com/1.1/search/tweets.json"
	params['request_type'] = "GET"
	params['count'] = "100"
	params['result_type'] = "recent"


	f = open("search_terms.txt",'rb')
	file_hash = hashlib.md5(f.read()).hexdigest()
	f.close()

	search_terms = {}
	search_terms = update_search_terms(search_terms)
	print(search_terms)

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	twitter_db = myclient["twitter_data"]
	collection = twitter_db["searched_tweets"]


	while(True):
		if (not check_update(file_hash)):
			search_terms = update_search_terms(search_terms)
		for each in search_terms:
			search_terms[each] = get_tweets(params, each, search_terms[each],collection)
		time.sleep()

main()






