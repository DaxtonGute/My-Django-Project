from django.urls import path

from . import views

app_name = 'social_app'
urlpatterns = [
    path('', views.HomePage.as_view(), name='HomePage'),
    path('sample-id-here/messages/', views.Messages.as_view(), name='Messages'),
]
