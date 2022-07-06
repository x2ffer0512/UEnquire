import requests
from bs4 import BeautifulSoup 
import pandas as pd
import json

def site(request):
	websitetwo='https://www.ue.edu.ph/mla/telephone-directory/'
	website_urltwo =requests.get(websitetwo, verify=False).text
	souptwo = BeautifulSoup(website_urltwo,'html.parser')
	my_tabletwo = souptwo.find('tbody')
	table_datatwo = []
	for rowtwo in my_tabletwo.findAll('tr'):
		row_datatwo = []
		for celltwo in rowtwo.findAll('td'):
			row_datatwo.append(celltwo.text)
		if(len(row_datatwo) > 0):
			data_itemtwo = {"DEPARTMENT": row_datatwo[0],
					 "LOCAL": row_datatwo[1],
					 "DIRECT LINE": row_datatwo[2]
					 }
			table_datatwo.append(data_itemtwo)

	dftwo = pd.DataFrame(table_datatwo, None)
	dtwo = dftwo.to_json(orient='records')
	datatwo = json.loads(dtwo)
	data2 = json.dumps(datatwo, indent=3)
	print(datatwo)

	allCoursetwo = []
	for coursetwo in datatwo:
		allCoursetwo.append((coursetwo['DEPARTMENT'].lower(), coursetwo['LOCAL'].lower(), coursetwo['DIRECT LINE']))
	def write__json(data, filename="twitter/intents.json"):
		with open (filename, 'w') as f:
			json.dump(data, f, indent=4)
	with open("twitter/intents.json") as json_file:
		datatwo = json.load(json_file)
		temptwo = datatwo["intents"]
		for itwo in allCoursetwo:
			ytwo = {"tag": itwo[0], "patterns": [itwo[0]], "responses": [itwo[1]]}
			temptwo.append(ytwo)
	write__json(datatwo)
	
	return request