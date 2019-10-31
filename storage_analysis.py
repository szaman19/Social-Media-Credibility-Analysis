import pymongo
import json
from datetime import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np

def main():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	twitter_db = myclient["twitter_data"]
	collection = twitter_db['streamed_tweets']


	dates = {}
	for document in collection.find():
		# document = json.loads(document)
		for each in document:
			if('timestamp_ms' in document.keys()):
				ts = int(document['timestamp_ms']) / 1000

				if (str(datetime.fromtimestamp(ts).date()) in dates):
					dates[str(datetime.fromtimestamp(ts).date())] +=1
				else:
					dates[str(datetime.fromtimestamp(ts).date())] =1

	# print(dates)
	

	log = open('output.txt', 'w')

	log.write("date,number of tweets\n")
	for each in dates.keys():
		string = each+","+str(dates[each])+"\n"
		log.write(string)
	log.close()


	y_pos = np.arange(len(dates.keys()))


	plt.bar(y_pos, dates.values(), align='center')
	plt.xticks(y_pos, dates.keys(), rotation='vertical')
	plt.ylabel("Number of tweets")
	plt.title("Daily Collection Graph")
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.25)
	# plt.show()
	plt.savefig("test.png", format="png")



main()