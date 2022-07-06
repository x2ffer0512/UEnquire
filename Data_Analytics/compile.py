import json 

with open("tentative.json", 'r') as data_file:
	data = json.load(data_file)

topics = []

for i in range(0, len(data["tweets"]), 2):
	topics.append(data["tweets"][i])

tweets_col = {}
topic_col = {}

col = 0 
elem = 1

while col < int(len(data["tweets"])/2):
	tweet = data["tweets"][elem].lower()
	string_unicode = tweet
	string_encode = string_unicode.encode("ascii", "ignore")
	tweet = string_encode.decode()



	tweets_col[col] = tweet
	elem += 2 
	col += 1 

for j in range(int(len(data["tweets"])/2)):
	topic_col[j] = topics[j]

new_data = {
	"tweets": tweets_col, "topic":topic_col
}	



with open("dataset.json", 'w') as data_file:
	json.dump(new_data, data_file, indent=4)
