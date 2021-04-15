from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import ConvoPreview
from .models import UserMessage
isGuest = False

class HomePage(TemplateView):
    template_name = "./social_app/HomePage.html"
    model = ConvoPreview
    def get_context_data(self,*args, **kwargs):
        context = super(HomePage, self).get_context_data(*args,**kwargs)
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['isGuest'] = isGuest
        return context

    #def get_queryset(self):
        # context = {'isGuest': isGuest,
        #            'ConvoPreview': ConvoPreview.objects}
        #return ConvoPreview.objects.all()

    def logIn():
        isGuest = False

    def logOut():
        isGuest = True
    # logIn = request.POST.get('logIn')
    # logOut = request.POST.get('logOut')
    # switch = request.POST.get('switchViews')
    # isGuest = False #how to access the global variable isGuest
    # if logIn:
    #     isGuest = False
    # if logOut:
    #     isGuest = True
    # if switch:
    #     isGuest = not isGuest

    # print("hi")
    # return render(request,'social_app/HomePage.html',{'isGuest': isGuest})

class Messages(TemplateView):
    template_name = "./social_app/Messages.html"
    # model = UserMessage
    def get_context_data(self,*args, **kwargs):
        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        return context
