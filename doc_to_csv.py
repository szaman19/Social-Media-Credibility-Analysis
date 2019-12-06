import pymongo
import json
from datetime import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
import tldextract

def main():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	twitter_db = myclient["twitter_data"]
	collection = twitter_db['streamed_tweets']
	# print(collection.count())
	f = open("domains.csv", 'w')
	f.write("domains \n")
	counter = 0
	for doc in collection.find():
		# print(doc.keys())
		if 'delete' not in doc.keys():
			if 'entities' in doc.keys():
				ent = doc['entities']
				# print(ent)
				if 'urls' in ent.keys():
					urls = ent['urls']
					if(len(urls) > 0):
						ext = tldextract.extract(urls[0]['expanded_url'])
						print(ext.domain)
						f.write(ext.domain)
						f.write('\n')
	f.close()
			 



main()