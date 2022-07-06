from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
from django.contrib.auth.models import User
import os
import random
import json

from tensorflow.keras.models import load_model
# ============================================================
import subprocess
from .models import *
from .forms import *
import re
# ============================================================
from twitter.forms import SourceForm, RegistrationForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password , check_password
from django.contrib import messages
from twitter.decorators import unauthenticated_user, allowed_users
# ============================================================
from django.views import View
from django.template import loader
# ============================================================
# from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from django.core.files.storage import FileSystemStorage

# ========================================================================================

class CrudView(ListView):
    model = Source
    template_name = 'twitter/Crud.html'
    context_object_name = 'source'

class CreateCrudUser(View):
    def  get(self, request):
    	name_source = request.GET.get('source_acct', None)
    	print(name_source)
    	obj = Source.objects.create(source_acct = name_source)
    	source = {'twitter_id':obj.twitter_id,'source_acct':obj.source_acct}
    	data = {'source': source}
    	return JsonResponse(data)

class linksViesUTwo(View):
    def  get(self, request):
    	link_name = request.GET.get('link_name', None)
    	links = request.GET.get('links', None)
    	obj = linksModel.objects.create(link_name = link_name, links = links)
    	source = {'link_id':obj.link_id,'link_name':link_name, 'links':obj.links}
    	data = {'source': source}
    	return JsonResponse(data)
# ========================================================================================
# UPLOAD DATASET FOR NAIVE BAYES 
from twitter.backend import training_classifier as classifier
from twitter.backend import uploads 
@login_required(login_url='twitter:login')
def upload(request):
	files = analyticsUpload.objects.all()
	uploadsF = ClassifierSettingsForm()
	context = {
		'files': files,
		'classifier_settings': ClassifierSettings.objects.all().last(),
		'model_desc': ClassifierModels.objects.all().last(),
		'uploadsF':uploadsF
	}
	if request.method == 'POST' and 'upload_dataset' in request.POST:
		request = uploads.naive_bayes_upload(request, analyticsUpload)

	# if request.method == 'POST' and 'upload_class' in request.POST:
	# 	upload_classify = request.FILES['upload_input']
		# upload_file = FileSystemStorage() #GINAGAWA NYANG FileSystemStorage PAG NAG UPLOAD KA ULIT NG PAREHAS NA FILE NAME PAPALITAN NYA YUN NG BAGONG FILE NAME
		# upload_file.save(upload_classify.name, upload_classify)
	
	
	# if request.method == 'POST' and 'upload_toClassify' in request.POST:
	# 	# TAKE NOTE: FIND A WAY TO SAVE AN INSTANCE OF A CLASS
	# 	pass

	return render(request, "twitter/upload_file/analytics_upload.html", context)

@login_required(login_url='twitter:login')
def trainClass(request):
	print("======================NEW CLSS =======================")
	if request.method == 'POST':
		test_size = request.POST['newTest']
		random_state = request.POST['random_state']
		average = request.POST['average']
		obj = ClassifierSettings(test_size=test_size, rand_state=random_state, average=average)
		obj.save()
		source = {'test_size':obj.test_size, 'rand_state':obj.rand_state, 'average':obj.average}
		data = {'source': source}
		return JsonResponse(data)
		
@login_required(login_url='twitter:login')
def train_Model(request):
	print("======================NEW TRAIN=======================")
	data_two = {}
	if request.method == 'POST':
		print("<<<<<<<<<<<<<<<<<< 111")
		file = request.POST['sub_train']
		file_obj = analyticsUpload.objects.get(name=file)
		print("<<<<<<<<<<<<<<<<<< 1222")
		if ClassifierSettings.objects.all().count() != 0:
			settings = ClassifierSettings.objects.all().last()
			print("<<<<<<<<<<<<<<<<<< 333")
			classifier_model, scores, vectorizer = classifier.naive_bayes(file_obj.file, settings.test_size, settings.rand_state, settings.average)
			print("<<<<<<<<<<<<<<<<<< 444")
			data_scores = pd.DataFrame([scores])
			print("<<<<<<<<<<<<<<<<<< 5555")
			d = data_scores.to_json(orient='records')
			data = json.loads(d)

			allScore = []
			for score in data:
				allScore.append((score['correct'], score['incorrect'], score['accuracy'],
					score['recall'], score['precision'], score['f1_score']))

			correct = None
			incorrect = None
			accuracy = None
			recall = None
			precision = None
			f1_score = None

			for i in allScore:
				correct = str(i[0])
				incorrect = str(i[1])
				accuracy = str(i[2])
				recall = str(i[3])
				precision = str(i[4])
				f1_score = str(i[5])

				sourceTwo = {'correct':correct, 'incorrect':incorrect, 'accuracy':accuracy, 'recall':recall,
				'precision':precision, 'f1_score':f1_score}

				print("TRAINING COMPLETE")
				message = "TRAINING COMPLETE"
				data_two = {'sourceTwo':sourceTwo, 'message':message}
			

			entry = ClassifierModels(
				correct=correct, incorrect=incorrect, accuracy=accuracy,
				recall=recall, precision=precision, f1_score=f1_score)
			entry.save()

		print(type(data_two))		
		return JsonResponse(data_two)

# ========================================================================================
# DOWNLOAD TWEETS EXCEL
from twitter.backend import download_file as dl
def download_excel(request):
	request = dl.excel_dl(Tweets)
	return request
# ========================================================================================
# TWITTER MAIN TABLE 
from twitter.backend import tw_backend as tw
@login_required(login_url='twitter:login')
def twitter_data(request):
	api = tw.open_acct()
	num_post = 1
	# Admin Inputs
	if request.method == 'POST' and 'num_posts' in request.POST:
		num_post = int(request.POST.get('number'))

	if request.method == 'POST' and 'sour_sub' in request.POST:
		sources = SourceForm(request.POST)
		# obj = sources.source_acct
		if sources.is_valid():
			sources.save()
		else:
			print("Invalid")
	if Source.objects.all().count() == 0:
		accounts = []
	else:
		accounts = Source.objects.all()
		accounts = tw.output(accounts, api, num_post)		
	# CONTEXT
	tweets = Tweets.objects.all()
	context = {'tweets': tweets, 'source_list': accounts}
	return render(request, "twitter/analytics.html", context)
# ========================================================================================
# INTENTS MAIN TABLE
from twitter.backend import training_chatbot as train_bot
# from twitter.backend import intents_backend as intent 
@login_required(login_url='twitter:login')
def intents(request):
	json_file = "twitter/intents.json"
	with open (json_file, "r") as file:
		data = json.load(file)
	form = Intents.objects.all()

	try:
		form[0]
	except IndexError:
		for item in data["intents"]:
			Intents(
				tag= item["tag"], pattern= item["patterns"], response= item["responses"], 
				context= item["context"], context_set= item["context_set"]
				).save()

	# TRAINING OF CHATBOT MODEL 
	if request.method == 'POST' and 'train_chatbot' in request.POST:
		train_bot.chatbot_training(request, ChatbotTuning)

	
	elif request.method == 'POST':
		print('asdadadadadadada')	
		def convert(string):
			clean = []
			if len(string) == 0:
				return []
			li = re.split(r',(?=")', string)
			for word in li:
				chars = list(word)
				if len(chars)!= 0:
					chars.pop(0)
					chars.pop()
				word = "".join(chars)
				clean.append(word)
			return clean
		
		tag = request.POST.get('tag')
		patterns = convert(request.POST.get('patterns'))
		responses = convert(request.POST.get('responses'))
		context = request.POST.get('context')
		context_set = convert(request.POST.get('context_set'))

		print("++++++++++++==")		
		form = Intents(tag=tag, pattern=patterns, response=responses, context=context, context_set=context_set)
		form.save()
		new_obj = {"tag": tag, "patterns": patterns, "responses": responses, "context": context, "context_set": context_set}
		

		data["intents"].append(new_obj) 
		with open("twitter/intents.json", 'w') as data_file:
			json.dump(data, data_file, indent=4)
		return JsonResponse({'new_form': new_obj})

	tuner = ''
	if  ChatbotTuning.objects.all().count() != 0:
		tuner = ChatbotTuning.objects.last()
	
	dictionary = {'intents': form, 'tuner': tuner}
	# ====================================================================
	return render(request, "twitter/chatbot_intents.html", dictionary)

from twitter.backend import training_chatbot as train_bot
def tuningForm(request):
	print("======================TRAINING TUNING=======================")
	if request.method == 'POST':
		train_bot.chatbot_training(request, ChatbotTuning)
		epoch = request.POST['id_input_epoch']
		rate = request.POST['id_input_lr']
		batch = request.POST['id_input_bs']
		obj = ChatbotTuning(epoch=epoch, rate=rate, batch=batch)
		obj.save()
		source = {'epoch':obj.epoch, 'rate':obj.rate, 'batch':obj.batch}
		data = {'source': source}
		return JsonResponse(data)


class intentsDeleteView(View):
	def get(self,request, pk, *args, **kwargs):
		if request.is_ajax():
			print("<<<<<=================DELETE========================")
			tag = Intents.objects.get(pk=pk)
			tag_name = str(tag.tag)
			tag.delete()
			with open("twitter/intents.json", "r") as file:
				data = json.load(file)	

			for item in data["intents"]:
				if item["tag"] == tag_name:
					data["intents"].remove(item)

			with open("twitter/intents.json", 'w') as data_file:
				json.dump(data, data_file, indent=4)

			return JsonResponse({"message":"success"})
		return JsonResponse({"message": "Wrong request"})

class sourcesDeleteView(View):
	def get(self,request, pk, *args, **kwargs):
		if request.is_ajax():
			print("<<<<<=================DELETE========================")
			source = Source.objects.get(pk=pk)
			source.delete()
			return JsonResponse({"message":"success"})
		return JsonResponse({"message": "Wrong request"})

class linksDeleteView(View):
	def get(self,request, pk, *args, **kwargs):
		if request.is_ajax():
			print("<<<<<=================DELETE========================")
			source = linksModel.objects.get(pk=pk)
			source.delete()
			return JsonResponse({"message":"success"})
		return JsonResponse({"message": "Wrong request"})
# ========================================================================================
#  WEBSCRAPING THE UE WEBSITE
from twitter.backend import ue_data 
def uedata(request):
	request = ue_data.site(request)
	return HttpResponse("UE DATA UPLOADED SUCCESSFULL")

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

# =======================================================================
@unauthenticated_user
def accounts_login(request, *args, **kwargs):
	context = {}
	if request.method=='POST' and 'signUp' in request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			# Account created successfully
			form.save()

			# After registration they are to be logged in
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email,password=raw_password)
			login(request,account,backend='django.contrib.auth.backends.ModelBackend')
			
			# san to nakuha??
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)

			messages.info(request, 'Account created successfully')
			return redirect("twitter:login")
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form

	
	destination = get_redirect_if_exists(request)
    #===============================================================================
	# SIGNIN 
	if request.method=='POST' and 'signIn' in request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			
			messages.info(request, 'You logged in.')
			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("twitter:chatbot-twitter-data")
			else: 
				print("--------------------------------------------")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "twitter/loginANDregister.html",context)

def logout_view(request):
	logout(request)
	return redirect("twitter:login")

def side(request):
	return render(request, "twitter/sidebar_and_head/sidebar.html")

@login_required(login_url='twitter:login')
def links(request):
	formTwo = linksModel.objects.all()
	context={'links':formTwo}
	return render(request, "twitter/links.html", context)
