from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from .models import ConvoPreview
from .models import UserMessage, UserProfile
from .forms import NewPostForm, SignUpForm
import datetime

class HomePage(TemplateView):
    template_name = "./social_app/HomePage.html"
    model = ConvoPreview
    def get_context_data(self,*args, **kwargs):
        context = super(HomePage, self).get_context_data(*args,**kwargs)
        context['ConvoPreview'] = ConvoPreview.objects.all()
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
            Author = request.user
            Date = datetime.date.today()
            postForm = NewPostForm()
            # args = {'Message': Message, 'Date': Date, 'Author': Author, 'Convo': Convo}
            for Convo in ConvoPreview.objects.all():
                 if Convo.Group_Name == GroupConvoID:
                    NewMessage = UserMessage.objects.create(Message_Text = Message, Time_Stamp = Date, Author = Author, GroupConvo = Convo)

        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        postForm = NewPostForm()
        context['NewPostForm'] = postForm
        return render(request, "./social_app/Messages.html",context)

class registration(TemplateView):
    template_name = "./registration/registration.html"

    def get_context_data(self,*args, **kwargs):
        context = super(registration, self).get_context_data(*args,**kwargs)
        form = SignUpForm()
        context['SignUpForm'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username,
                                 email=email,
                                 password=password)
            login(request, user)
            return redirect('../')
        else:
            form = SignUpForm()
        return render(request, './registration/registration.html', {'SignUpForm': form})
