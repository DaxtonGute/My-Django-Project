from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from . import views

app_name = 'social_app'
urlpatterns = [
    path('', views.HomePage.as_view(), name='HomePage'),  # Home page does not have a path
    path('messages/<GroupConvoID>/', views.Messages.as_view(), name='Messages'), # Each message has a custom id and that is stated in its path
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name':'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^registration/$', views.registration.as_view(), {'template_name': 'registration/registration.html'}, name='registration'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
