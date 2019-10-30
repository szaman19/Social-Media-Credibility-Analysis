#!/bin/sh

while true 
do
	touch user.err
	python twitter_user_data.py 2>user.err;
	if [ -s user.err ]
	then 
		echo "Search request failed" | mail -s "Twitter Search Daemon" szaman5@binghamton.edu
		break
	fi
	#statements
done