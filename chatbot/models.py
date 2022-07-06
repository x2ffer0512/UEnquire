from django.db import models
import os, random
import uuid

LOCATION = (
	('Recto Gate', 'RECTO GATE'), 
	('Gastambide Gate', 'GASTAMBIDE GATE')
)

CHOICES = (('L', 'Lost'), ('F', 'Found'))



# Create your models here.

class UserSession(models.Model):
	user_name = models.CharField(max_length=100, verbose_name='User Name')
	gender = models.CharField(max_length=50, verbose_name='Gender')
	user_text = models.TextField(verbose_name='User Input', null=True)
	user_session = models.CharField(max_length=150,verbose_name='User Session', null=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	visits = models.IntegerField(verbose_name="Number of visit", null=True)
	class Meta:
		db_table = "user_session"

	def __str__(self):
		return self.user_name

	def get_abolute_url(self):
		return "/chatbot/%i/" % self.id
	def detail(self):
		return f"Username: {self.user_name}, gender: {self.gender}, Session: {self.user_session}"


#LOST N FOUND TABLE
class LostNFound(models.Model):
	reg_id = models.AutoField(primary_key=True, verbose_name='ID')
	name = models.CharField(max_length=100, verbose_name='Name')
	stud_num = models.CharField(max_length=11, verbose_name = "Student Number", blank=True)
	email = models.EmailField(max_length=50, verbose_name='Email', blank=True)
	contact = models.CharField(max_length=11, verbose_name='Contact Number')
	lost_and_found = models.CharField(max_length=100, verbose_name='Lost & Found' ,choices=CHOICES)
	lostNfound_date = models.DateField(verbose_name='Date')
	lostNfound_time = models.TimeField(verbose_name="Time", blank="True", null="True")

	item = models.CharField(max_length=100,verbose_name='Item')

	item_desc = models.TextField(max_length=500,verbose_name='Item Description')  
	pick_up_loc = models.CharField(max_length=100, verbose_name='Pick-up Location',choices=LOCATION, default='RECTO GATE')


	claimed = models.BooleanField(default=False, verbose_name="Claimed")
	receiver = models.CharField(max_length=100, verbose_name='Received by', blank="True", null="True")
	received_date = models.DateField(verbose_name='Date',  blank="True", null="True")
	received_time = models.TimeField(verbose_name="Time", blank="True", null="True")

	def __str__(self):
		return self.name

	def __unicode__(self):
		return "%s (%s : %s)" % (self.name, self.date_start.strftime('%I:%M %p'), self.lostNfound_time)

class FeedBack(models.Model):
	feedback_name = models.CharField(max_length=100, verbose_name='Name')
	feedback_email = models.CharField(max_length=100, verbose_name='Email')
	feedback_subject = models.CharField(max_length=100, verbose_name='Subject')
	feedback_message = models.TextField(max_length=500,verbose_name='Message')

	def __str__(self):
		return self.feedback_name



