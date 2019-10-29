import requests as r 
import base64
from random import getrandbits 
import hmac 
import hashlib
import urllib.parse as up
import time 
import secrets

class Request(object):
	"""
	docstring for Twitter-Request
	
	...

	Attributes
	----------
	oauth_consumer_key: str
	oauth_consumer_secret: str
	oauth_access_key: str
	oauth_access_key_secret: str
	oauth_url: str
	oauth_type: str

	Methods
	--------------

	gen_request()
		Returns a Request object with generated OAuth1.0 headers

	"""
	def __init__(self, params, search = False):
		"""
		Parameters
		----------
		params : dict
			Dictionary of SIX key:value pairs. 
			oauth_consumer_key: str
			oauth_consumer_secret: str
			oauth_access_key: str
			oauth_access_key_secret: str
			oauth_url: str
			oauth_type: str
		"""
		super(Request, self).__init__()
		self.oauth_consumer_key = params["oauth_consumer_key"]
		self.oauth_access_key = params["oauth_access_key"]
		self.oauth_consumer_key_secret = params["oauth_consumer_key_secret"]
		self.oauth_access_key_secret = params["oauth_access_key_secret"]		

		self.url = params['url']
		self.type = params['request_type']
		self.search_params = {}

		if(search):
			self.search_params['q'] = params['q']
			self.search_params['count'] = params['count']


	def get_time_stamp(self):
		return int(time.time())

	def encode(self, byte_str):
		return up.quote(str(byte_str), safe="")
	
	def get_nonce(self):
		return str(getrandbits(64))
	
	def create_signature(self, params, signing_key):
		signature_base = ""
		signature_base += self.type
		signature_base += "&"
		signature_base += self.encode(self.url)
		signature_base += "&"

		if(self.search_params):
			for key in self.search_params.keys():
				params[key] = self.search_params[key]

		param_string = '&'.join([('%s=%s' % (self.encode(str(k)), self.encode(str(params[k])))) for k in sorted(params)])

		print(param_string)
		message = signature_base + self.encode(param_string)

		message = bytes(message,'UTF-8')
		signing_key = bytes(signing_key,'UTF-8')

		signature = hmac.new(signing_key, message, hashlib.sha1).digest()

		sig_base_64 = base64.urlsafe_b64encode(signature)

		# print(sig_base_64.decode("utf-8"))

		return sig_base_64.decode("utf-8")	

	def get_request(self, stream = True, custom_query = False):
		params = {}
		params["oauth_consumer_key"] = self.oauth_consumer_key
		params["oauth_token"] = self.oauth_access_key
		params["oauth_version"] = "1.0"
		params["oauth_nonce"] = self.get_nonce()
		params["oauth_timestamp"] = self.get_time_stamp()
		params["oauth_signature_method"] = "HMAC-SHA1"

		signing_key =  self.oauth_consumer_key_secret +"&"+ self.oauth_access_key_secret

		params["oauth_signature"] = self.create_signature(params, signing_key)

		DST = "OAuth "
		auth_param_str = ", ".join(['%s="%s"' % (self.encode(i) , self.encode(params[i])) for i in sorted(params)])
		
		DST += auth_param_str

		# print(DST)

		headers = {}
		headers['authorization'] = DST.rstrip('\n')
		req = r.Request(self.type, self.url, headers=headers)
		
		if(custom_query):
			req = r.Request(self.type, self.url, headers=headers, params=self.search_params)
			return req
		return req