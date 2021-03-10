from django.shortcuts import render
from django.http import HttpResponse

def HomePage(request):
    return render(request,'social_app/HomePage.html')

def Messages(request):
    return render(request,'social_app/Messages.html')
