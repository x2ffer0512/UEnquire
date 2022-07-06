from django.urls import path
from django.urls import reverse
from . import views
import twitter.views

app_name = 'chatbot'

urlpatterns = [
    path("chatbot/<uuid>/", views.chatbot, name='chatbot_chatbot'),
    path("post/<uuid>/", views.chatbot_process, name='post'),
    path("feed_create/", views.createFeedback, name='create'),
    path("lost_found_create/", views.lostFount, name='lost_found'),
    path("sample/", views.sample, name='sample'),
    path("", views.landing, name='home'),
    path("rule/", views.filter_acct, name='rule'),
    path("data_privacy/", views.data_privacy, name='data_privacy'),

]
