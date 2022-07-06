import os 
from django.contrib import messages

def validate(request, value, table):
	valid_extensions = ['.xlsx', '.xls', '.csv', '.json']
	name, extension = os.path.splitext(value.name)
	if extension.lower() not in valid_extensions:
		messages.info(request, 'Invalid File Upload')
		print("MAli file")
		return None, None, request
	elif table.objects.filter(name=name).filter(file_type= extension):
		messages.info(request, 'File already exist.')
		print("doble file")
		return None, None, request
	else:	
		return name, extension, request

def naive_bayes_upload(request, table):
	upload_file = request.FILES['file']
	name, extension, request = validate(request, upload_file, table)
	if name != None and extension != None:
		form = table(name=name, file_type= extension, file = upload_file)
		form.save()
	return request