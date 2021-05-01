from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from .models import ConvoPreview, UserMessage, UserWrapper
from .forms import NewPostForm, SignUpForm, DeleteMessage, StarGroupConvo
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
    slug_url_kwarg = 'GroupConvoID'

    def get_context_data(self,*args, **kwargs):
        print(*args)
        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['UserWrapper'] = UserWrapper.objects.all()
        postForm = NewPostForm()
        context['NewPostForm'] = postForm
        deleteForm = DeleteMessage()
        context['DeleteMessage'] = deleteForm
        starForm = StarGroupConvo()
        context['StarGroupConvo'] = starForm

        # isMatch = False
        # for user in UserWrapper.objects.all():
        #     if user.user.id == request.user.id: #getting correct user
        #         for convo in user.starredGroupConvos:
        #             if convo.GroupId == val:   #getting correct ConvoPreview
        #                 isMatch = True
        #                 convoToRemove = convo
        #                 break
        #
        # print(slug_url_kwarg)
        return context

    def post(self, request, *args, **kwargs):
        for key, value in kwargs.items():
            GroupConvoID = value #since there is only one

        deleteForm = DeleteMessage(request.POST)
        if deleteForm.is_valid():
            val = deleteForm.cleaned_data.get("deleteBtn")
            for message in UserMessage.objects.all():
                if str(message) == str(val):
                    message.delete()
        deleteForm = DeleteMessage()


        starForm = StarGroupConvo(request.POST)
        if starForm.is_valid():
            val = starForm.cleaned_data.get("star")
            isunStarred = False
            print("what")
            for user in UserWrapper.objects.all():
                print("hi")
                print(request.user)
                if user.user.id == request.user: #getting correct user
                    print(request.user)
                    for convo in user.starredGroupConvos.all():
                        if str(convo.GroupId) == val:   #getting correct ConvoPreview
                            isunStarred = True
                            convoToRemove = convo
                            break
            if isunStarred:
                user.starredGroupConvos.remove(convoToRemove)
            else:
                for convo in ConvoPreview.objects.all():
                    if str(convo.GroupId) == val: #getting correct ConvoPreview
                        for user in UserWrapper.objects.all():
                            if user.user.id == request.user.id: #getting correct user
                                user.starredGroupConvos.add(convo)
                                break


        starForm = DeleteMessage()

        postForm = NewPostForm(request.POST)
        if postForm.is_valid():
            Message = postForm.cleaned_data['Message']
            Author = request.user
            Date = datetime.date.today()
            postForm = NewPostForm()
            # args = {'Message': Message, 'Date': Date, 'Author': Author, 'Convo': Convo}
            for Convo in ConvoPreview.objects.all():
                 if str(Convo.GroupId) == GroupConvoID:
                    NewMessage = UserMessage.objects.create(Message_Text = Message, Time_Stamp = Date, Author = Author, GroupConvo = Convo)
        postForm = NewPostForm()

        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['UserWrapper'] = UserWrapper.objects.all()
        context['NewPostForm'] = postForm
        context['DeleteMessage'] = deleteForm
        context['StarGroupConvo'] = starForm
        context['starred'] = not isunStarred
        return render(request, "./social_app/Messages.html",context)

class registration(TemplateView):
    template_name = "./registration/registration.html"

    def get_context_data(self,*args, **kwargs):
        context = super(registration, self).get_context_data(*args,**kwargs)
        signUpForm = SignUpForm()
        context['SignUpForm'] = signUpForm
        return context

    def post(self, request, *args, **kwargs):
        signUpForm = SignUpForm(request.POST)
        if signUpForm.is_valid():
            user = signUpForm.save()
            user.refresh_from_db()
            user.save()
            password = signUpForm.cleaned_data.get('password1')
            email = signUpForm.cleaned_data.get('email')
            username = signUpForm.cleaned_data.get('username')
            user = authenticate(username=username,
                                 email=email,
                                 password=password)
            UserWrapper.objects.create(user = user)
            login(request, user)
            return redirect('../')
        else:
            signUpForm = SignUpForm()

        return render(request, './registration/registration.html', {'SignUpForm': signUpForm})
