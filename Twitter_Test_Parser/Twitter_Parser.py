import requests as r
import base64
import json
from random import getrandbits
import hmac 
import hashlib
import urllib.parse
import time
import secrets
from requests_oauthlib import OAuth1Session
import json
import Twitter_Request

def get_tokens(file_name=".cert"):
	certification_file = open(file_name, "r")
	tokens = {}
	counter = 0

	keys = ["API","API_SECRET","ACCESS","ACCESS_SECRET"]

	for lines in certification_file:
		line = lines.strip().rstrip('\n').split()
		if(len(line) > 1):
			print("Failed reading certification file")
		else:
			tokens[keys[counter]] = line[0]
			counter +=1
	certification_file.close()

	return tokens

def main():
	tokens = get_tokens()
	# try_outh(tokens)
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

	for line in resp.iter_lines():
		if(line):
			line = line.decode('utf-8')
			d = json.loads(line)
			print(d)

main()
