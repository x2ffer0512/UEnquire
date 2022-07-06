from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

from .models import *
# Register your models here.

class User(admin.ModelAdmin):
	list_display = ['user_name','gender', 'user_text']
	search_fields = ['user_name','gender']
	readonly_fields = ['user_session', 'uuid', 'visits']

class LostNFoundAdmin(admin.ModelAdmin):
	list_display = ['name', 'stud_num', 'email', 'contact', 'lost_and_found', 'item', 'item_desc', 'pick_up_loc', 'claimed', 'receiver']
	search_fields = ['name','stud_num', 'email',' lost_and_found','item']
	radio_fields = {"lost_and_found": admin.VERTICAL}

	

class FeedBackAdmin(admin.ModelAdmin):
	list_display = ['feedback_name','feedback_email','feedback_subject','feedback_message']
	search_fields = ['feedback_name', 'feedback_email']
	
admin.site.register(UserSession, User)
admin.site.register(LostNFound, LostNFoundAdmin)
admin.site.register(FeedBack, FeedBackAdmin)
