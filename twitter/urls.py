from django.urls import path
from . import views
from .views import (intentsDeleteView,sourcesDeleteView,linksDeleteView)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'twitter'

urlpatterns = [
    path("dashboard/", views.twitter_data, name = "chatbot-twitter-data"),
    path("intents/", views.intents, name = "intents"),
    path("uedata/", views.uedata, name='uedata'),
    path("login/",views.accounts_login, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path("intents/<int:pk>/", intentsDeleteView.as_view(), name="updata_delete"),
    path("twitter/<int:pk>/", sourcesDeleteView.as_view(), name="source_delete"),
    path("links/<int:pk>/", linksDeleteView.as_view(), name="links_delete"),


    path("side/", views.side, name="side"),

    
    path("Naive_bayes_Trainer/", views.upload, name="upload_file"),

    path("download_excel/", views.download_excel, name="download_excel"),
    

    path('crud/', views.CrudView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/', views.CreateCrudUser.as_view(), name='crud_ajax_create'),

    path('links/', views.links, name="links"),
    path('ajax/crud/links/', views.linksViesUTwo.as_view(), name='linksViesUTwo'),
    path("classifier_create/", views.trainClass, name='classifier'),
    path("train_Model/", views.train_Model, name='train_model'),
    path("tuning_form/", views.tuningForm, name='tuning'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)