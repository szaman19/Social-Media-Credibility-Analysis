#!/bin/sh

while true 
do
	touch search.err
	python twitter_search_data.py 2>search.err;
	if [ -s search.err ]
	then 
		echo "Search request failed" | mail -s "Twitter Search Daemon" szaman5@binghamton.edu
		break
	fi
	#statements
done