import tldextract
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.neighbors import KernelDensity

def bias_check(sources):
	fd = pd.read_csv("domains_search.csv")
	topn = fd['domains']

	rval = {}
	rval['left'] = 0
	rval['right'] = 0
	rval['extreme-right'] = 0
	rval['extreme-left'] = 0
	rval['center'] = 0
	rval['right-center'] = 0
	rval['left-center'] = 0


	total = 0
	for each in topn:
		if (each in sources.keys()):
			bias = sources[each][1]
			rval[bias] +=1
			total +=1
	# print(rval)
	
	vec = ["extreme-left", 'left',"left-center", 'center', 'right-center', 'right', 'extreme-right']
	vals = []
	data_points = []
	counter = 0
	for each in vec:
		vals.append((each,rval[each]))
		temp = [counter] * rval[each]
		counter +=1
		data_points = data_points + temp

	kernel = 'exponential'
	data_points = np.array(data_points)[:, np.newaxis]

	kde = KernelDensity(kernel=kernel, bandwidth=.2).fit(data_points)
	X_plot = np.linspace(0, 7, 10000)[:, np.newaxis]
	
	print(kde.get_params(deep=True))
	pdf = kde.score_samples(X_plot)
	# kde = KernelDensity(kernel='cosine', bandwidth=1).fit(data_points)
	# cos_pdf = kde.score_samples(X_plot)



	plt.bar([x[0] for x in vals], [x[1]/total for x in vals], align='edge')
	plt.plot(X_plot[:,0],np.exp(pdf) , color = 'r', label = "Exponential KDE")
	# plt.plot(X_plot[:,0],np.exp(cos_pdf) , color = 'g', label = "Cosine KDE")
	
	plt.title("Polarization in Political Twitter ")
	plt.legend()
	
	plt.savefig("t.png")



def quality_check():
	print("tbi")

def main():
	f = open("corpus.csv","r")
	sources = {}

	counter = 0
	for lines in f:
		if (counter > 0):
			lines = lines.split(",")
			ext = tldextract.extract(lines[1])
			sources[ext.domain] = (lines[3], lines[4].strip())
			# print(ext.domain, lines[3], lines[4])
		counter +=1
	bias_check(sources)


main()