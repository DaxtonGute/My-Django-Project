from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url

from . import views

app_name = 'social_app'
urlpatterns = [
    path('', views.HomePage.as_view(), name='HomePage'),
    path('sample-id-here/messages/', views.Messages.as_view(), name='Messages'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
