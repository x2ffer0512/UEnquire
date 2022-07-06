from django import forms
from django.forms import ModelForm
from chatbot.models import *

class UserSessionForm(ModelForm):
	class Meta:
		model = UserSession
		fields = ['user_name', 'gender']


class UserSessionTwoForm(ModelForm):
	class Meta:
		model = UserSession
		fields = ['user_text']

class UserSessionVisit(ModelForm):
	class Meta:
		model = UserSession
		fields = ['visits']

class UserSessionUserS(ModelForm):
	class Meta:
		model = UserSession
		fields = ['user_session']

class FeedbackForm(ModelForm):
	class Meta:
		model = FeedBack
		fields = '__all__'

class LostANDFound(ModelForm):
	class Meta:
		model = LostNFound
		fields = ['name', 'stud_num', 'email', 'contact', 'lost_and_found', 'item', 'item_desc', 'pick_up_loc']
		widgets = {
            'lost_and_found': forms.RadioSelect,
        }
