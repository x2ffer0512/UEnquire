from django import forms
from django.forms import ModelForm
from twitter.models import *

from django.contrib.auth import authenticate
from django.contrib.auth import views
import os


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

class ClassifierSettingsForm(ModelForm):
	class Meta:
		model = ClassifierSettings
		fields = ['average']

class linksForm(ModelForm):
	class Meta:
		model = linksModel
		fields = ['link_name', 'links']

class anaUploadForm(forms.FileField):
	filename = models.CharField(max_length=200)
	json_file = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}),)
	class Meta:
		model = analyticsUpload
		fields = '__all__'

class IntentsForm(ModelForm):
	class Meta:
		model = Intents
		fields = ["tag", "pattern", "response", "context", "context_set"]

class SourceForm(ModelForm):
	class Meta:
		model = Source
		fields = ['source_acct']


#ACCOUNT AUTHENTICATION
class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
	class Meta:
		model = Account
		fields = ('username', 'email', 'password1', 'password2',)

	def clean_email(self):

		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except  Exception as e:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
