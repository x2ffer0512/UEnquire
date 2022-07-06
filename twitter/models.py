from django.db import models
import os, random

from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# =============================================================================================
# FILE UPLOADS
CLASS = (
	('macro', 'macro'), 
	('micro', 'micro'),
	('None', 'None'),
	('weighted', 'weighted'),
	('samples', 'samples'),
)

class linksModel(models.Model):#DONE
	link_id = models.AutoField(primary_key=True, verbose_name='Links ID')
	link_name = models.CharField(max_length=200, verbose_name='Links Name')
	links = models.CharField(max_length=500, verbose_name='Links')



class analyticsUpload(models.Model):#DONE
	file_id = models.AutoField(primary_key=True, verbose_name='File ID')
	name = models.CharField(max_length=200, verbose_name='File Name')
	file_type = models.CharField(max_length=200, verbose_name='File Extension')
	file = models.FileField(upload_to='twitter/upload_file/', verbose_name='File')
	
	def __str__(self):
		return self.name
# =============================================================================================
class ClassifierSettings(models.Model):#DONE
	# ADMIN INPUT
	test_size = models.CharField(max_length=200, verbose_name= 'Test Size')
	rand_state = models.CharField(max_length=200, verbose_name= 'Random State')
	average = models.CharField(max_length=200, verbose_name= 'Average', choices=CLASS, default='macro')
# =============================================================================================
class ChatbotTuning(models.Model):#DONE
	id_model = models.AutoField(primary_key=True, verbose_name='Chatbot ID')
	# Tuning settings 
	epoch = models.CharField(max_length=200, verbose_name= 'Epoch')
	rate = models.CharField(max_length=200, verbose_name= 'Learning Rate')
	batch = models.CharField(max_length=200, verbose_name= 'Batch Size')
	# ACCURACY 
	# train_accuracy = models.CharField(max_length=200, verbose_name= 'Training Accuracy') 
	# train_loss = models.CharField(max_length=200, verbose_name= 'Training Loss') 
# =============================================================================================
class ClassifierModels(models.Model):#DONE
	id_model = models.AutoField(primary_key=True, verbose_name='model ID ')

	# SCORES 
	correct = models.CharField(max_length=200, verbose_name= 'Correct')
	incorrect = models.CharField(max_length=200, verbose_name= 'Incorrect')
	accuracy = models.CharField(max_length=200, verbose_name= 'Accuracy')
	recall = models.CharField(max_length=200, verbose_name= 'Recall')
	precision = models.CharField(max_length=200, verbose_name= 'Precision')
	f1_score = models.CharField(max_length=200, verbose_name= 'F1_Score')
# =============================================================================================
# TWEETS TABLE
class Tweets(models.Model):#DONE
	post_id = models.AutoField(primary_key=True, verbose_name='Post ID')
	
	source = models.CharField(max_length=500, verbose_name='Twitter Source')

	posts = models.CharField(max_length=500, verbose_name='Raw tweet')
	likes =  models.CharField(max_length=10, verbose_name='Likes')
	dates = models.CharField(max_length=30, verbose_name="Date Created" )
	time = models.CharField(max_length=30, verbose_name="Time Created" )


	tags = models.CharField(max_length=500, null=True, verbose_name="Hashtags" )
	links = models.CharField(max_length=200, null=True, verbose_name="Links" )

	def __str__(self):
		return str(self.post_id) if self.post_id else ''

	def detail(self):
		return f"post_id: {self.post_id}, source: {self.source}, posts: {self.posts}"
# =============================================================================================
# SOURCE TABLE
class Source(models.Model): #DONE
	twitter_id = models.AutoField(primary_key=True, verbose_name='Twitter ID')
	source_acct = models.CharField(max_length=250, verbose_name='Twitter Accounts')

	def __str__(self):
		return self.source_acct
# =============================================================================================
# INTENTS TABLE
class Intents(models.Model):#DONE
	id_tag = models.AutoField(primary_key=True, verbose_name='Tag ID')
	tag = models.CharField(max_length=500, null=True, verbose_name="Tag" )
	pattern = models.CharField(max_length=3000, null=True, verbose_name="pattern" )
	response = models.CharField(max_length=3000, null=True, verbose_name="response" )
	context = models.CharField(max_length=500, null=True, blank=True, verbose_name="context" )
	context_set = models.CharField(max_length=500, null=True, blank=True, verbose_name="context" )

	def __str__(self):
		return self.tag
# =============================================================================================
class MyAccountManger(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have an username.")
		
		user = self.model(
			email=self.normalize_email(email),
			username=username,
			)
		
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

# class Account(AbstractBaseUser, PermissionsMixin):
class Account(AbstractBaseUser):#DONE
	account_id = models.AutoField(primary_key=True, verbose_name='Account ID',unique=True)
	email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
	username = models.CharField(max_length=100, unique=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	
	hide_email = models.BooleanField(default=True)

	object = MyAccountManger()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username
	
	@property
	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True
