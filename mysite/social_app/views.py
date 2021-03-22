from django.shortcuts import render
from django.http import HttpResponse
isGuest = False

def HomePage(request):
    logIn = request.POST.get('logIn')
    logOut = request.POST.get('logOut')
    switch = request.POST.get('switchViews')
    isGuest = False #how to access the global variable isGuest
    if logIn:
        isGuest = False
    if logOut:
        isGuest = True
    if switch:
        isGuest = not isGuest

    print("hi")

    return render(request,'social_app/HomePage.html',{'isGuest': isGuest})

def Messages(request):
    return render(request,'social_app/Messages.html')
