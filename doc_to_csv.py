import pymongo
import tldextract

def main():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	twitter_db = myclient["twitter_data"]
	collection = twitter_db['url_tweets_test']
	# print(collection.count())
	f = open("domains_search.csv", 'w')
	f.write("domains,suffix,subdomain,reg_domain\n")
	counter = 0
	tweets = collection.find()
	total  = tweets.count()
	for doc in tweets:
		counter +=1
		print("Analyzing: ", counter , " / ", total)
		if 'delete' not in doc.keys():
			if 'entities' in doc.keys():
				ent = doc['entities']
				# print(ent)
				if 'urls' in ent.keys():
					urls = ent['urls']
					if(len(urls) > 0):
						ext = tldextract.extract(urls[0]['expanded_url'])
						f.write(ext.domain)
						f.write(",")
						f.write(ext.suffix)
						f.write(",")
						f.write(ext.subdomain)
						f.write(",")
						f.write(ext.registered_domain)
						f.write('\n')
	f.close()
			 



main()
