import requests as r
import base64
import json

def get_tokens(file_name=".cert"):
	certification_file = open(file_name, "r")
	tokens = {}
	counter = 0

	keys = ["API","API_SECRET","ACCESS","ACCESS_SECRET"]

	for lines in certification_file:
		line = lines.strip().split()
		if(len(line) > 1):
			print("Failed reading certification file")
		else:
			tokens[keys[counter]] = line[0]
			counter +=1
	certification_file.close()

	return tokens

def get_bearer_token(tokens):
	token_credentials = tokens["API"] +":"+tokens["API_SECRET"]
	token_credentials = "Basic " + str(base64.urlsafe_b64encode(token_credentials.encode()), "utf-8")

	print(token_credentials)

	headers = {"Authorization":token_credentials, 
	"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
	"Host":"api.twitter.com",
	"Accept-Encoding": "gzip"}
	request_params = {"grant_type":"client_credentials"}
	response = r.post("https://api.twitter.com/oauth2/token", headers=headers, data=request_params)
	print(response.text)
	json_data = json.loads(response.text)[0]
	tokens ['bearer_token'] = json_data["access_token"]
	return tokens

def get_request(b_tokens):

	print(b_tokens)

	session = r.Session()

def main():
	tokens = get_tokens()
	tokens = get_bearer_token(tokens)
	get_stream(tokens)
main()