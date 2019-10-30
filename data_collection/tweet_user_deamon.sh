#!/bin/sh

while true 
do
	python collect_user_data.py 2>user.err;
	if [ -s user.err ]
	then 
		echo "Search request failed" | mail -s "Twitter Search Daemon" szaman5@binghamton.edu
		break
	fi
	#statements
done