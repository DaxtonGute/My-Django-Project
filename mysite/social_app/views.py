from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import ConvoPreview
from .models import UserMessage
from .forms import NewPostForm
import datetime
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
    model = UserMessage
    def get_context_data(self,*args, **kwargs):
        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        postForm = NewPostForm()
        context['NewPostForm'] = postForm
        return context

    def post(self, request, *args, **kwargs):
        for key, value in kwargs.items():
            GroupConvoID = value #since there is only one

        postForm = NewPostForm(request.POST)
        if postForm.is_valid():
            Message = postForm.cleaned_data['Message']
            Author = postForm.cleaned_data['Author']
            Date = datetime.date.today()
            postForm = NewPostForm()
            GroupConvoActualID = 0
            for Convo in ConvoPreview.objects.all():
                if Convo.Group_Name == GroupConvoID:
                    GroupConvoActualID = Convo
            args = {'Message': Message, 'Date': Date, 'Author': Author, 'Convo': Convo}
            NewMessage = UserMessage(args)

        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        postForm = NewPostForm()
        context['NewPostForm'] = postForm
        return render(request, "./social_app/Messages.html",context)
