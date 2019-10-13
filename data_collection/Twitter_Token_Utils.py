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