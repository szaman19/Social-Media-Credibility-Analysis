import pymongo 
import Twitter_Request
import requests as r
import json
import Twitter_Token_Utils
def main():
	tokens = Twitter_Token_Utils.get_tokens()
	params = {}
	params["oauth_consumer_key"] = tokens['API']
	params["oauth_access_key"] = tokens ['ACCESS']
	params["oauth_consumer_key_secret"] = tokens["API_SECRET"]
	params["oauth_access_key_secret"] = tokens ["ACCESS_SECRET"]

	params['url'] = "https://stream.twitter.com/1.1/statuses/sample.json"
	params['request_type'] = "GET"

	TR = Twitter_Request.Request(params).get_request()

	TR = TR.prepare()

	session = r.Session()

	resp = session.send(TR,  stream=True)
	print(resp.status_code)

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	twitter_db = myclient["twitter_data"]

	collection = twitter_db["streamed_tweets"]
	
	counter = 0
	for line in resp.iter_lines():
		if(line):
			line = line.decode('utf-8')
			d = json.loads(line)
			# print(d)
			if('delete' not in d):
				#print("detected not deleted tweet, adding", counter)
				collection.insert_one(d)
				counter +=1
				if (counter % 100 == 0):
					print("Number of tweets collected: ", counter)
			#else:
				#print("detected deleted tweet")
		if (counter == 3000000):
			break

	session.close()

	# x = collection.find().limit(10)

	# for i in x:
	# 	print(i)


if __name__ == '__main__':
	main()
