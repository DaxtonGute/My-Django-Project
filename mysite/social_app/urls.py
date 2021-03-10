from django.urls import path

from . import views

app_name = 'social_app'
urlpatterns = [
    path('', views.HomePage, name='HomePage'),
    path('sample-id-here/messages/', views.Messages, name='Messages'),
]
