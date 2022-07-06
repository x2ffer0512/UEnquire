# import json 
# import re 
# from twitter.models import *
# def open_intents(table):
# 	json_file = "twitter/intents.json"
# 	with open (json_file, "r") as file:
# 		data = json.load(file)
# 	table.objects.all().delete()

# 	for item in data["intents"]:
# 		table(tag= item["tag"], pattern= item["patterns"], response= item["responses"], 
# 			context= item["context"], context_set= item["context_set"]).save()
	
# 	form = table.objects.all()
# 	return form, data

# def request_POST(request, data):
# 	def convert(string):
# 		clean = []
# 		if len(string) == 0:
# 			return []
# 		li = re.split(r',(?=")', string)
# 		for word in li:
# 			chars = list(word)
# 			if len(chars)!= 0:
# 				chars.pop(0)
# 				chars.pop()
# 			word = "".join(chars)
# 			clean.append(word)
# 		return clean
		
# 	tag = request.POST.get('tag')
# 	patterns = convert(request.POST.get('patterns'))
# 	responses = convert(request.POST.get('responses'))
# 	context = request.POST.get('context')
# 	context_set = convert(request.POST.get('context_set'))

# 	form = Intents(tag=tag, pattern=patterns, response=responses, context=context, context_set=context_set)
# 	form.save()
# 	new_obj = {"tag": tag, "patterns": patterns, "responses": responses, "context": context, "context_set": context_set}
	

# 	data["intents"].append(new_obj) 

# 	return form, new_obj, data, request
