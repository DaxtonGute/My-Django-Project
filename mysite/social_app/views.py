from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from .models import ConvoPreview, UserMessage, Post_Likes
from .forms import NewPostForm, NewConvoForm, SignUpForm, DeleteMessage, StarGroupConvo
import datetime

class HomePage(TemplateView):
    template_name = "./social_app/HomePage.html"
    model = ConvoPreview
    def get_context_data(self,*args, **kwargs):
        dictionaryOfLikes = {}
        for groupConvo in ConvoPreview.objects.all():
            for postLike in Post_Likes.objects.all():
                if postLike.user == self.request.user and postLike.post == groupConvo:
                    dictionaryOfLikes[groupConvo.GroupId] = True
            if dictionaryOfLikes.get(groupConvo.GroupId) is None:
                dictionaryOfLikes[groupConvo.GroupId] = False

        favorites = []
        for postLike in Post_Likes.objects.all():
            if postLike.user == self.request.user:
                favorites.append(postLike)

        context = super(HomePage, self).get_context_data(*args,**kwargs)
        starGroupConvo = StarGroupConvo()
        context['StarGroupConvo'] = starGroupConvo
        convoForm = NewConvoForm()
        context['NewConvoForm'] = convoForm
        context['Dictionary'] = dictionaryOfLikes.copy()
        context['favorites'] = favorites
        context['ConvoPreview'] = ConvoPreview.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        starGroupConvo = StarGroupConvo(request.POST)
        if starGroupConvo.is_valid() and starGroupConvo.cleaned_data['star'] != "":
            GroupConvoID = starGroupConvo.cleaned_data['star']
            post = ConvoPreview.objects.get(GroupId=GroupConvoID)
            number_of_likes = Post_Likes.objects.filter(user=request.user, post=post).count()
            if number_of_likes > 0:
                already_liked = True # pass this variable to your context
                Post_Likes.objects.filter(user=request.user, post=post).delete()
            else:
                already_liked = False # you can make this anything other than boolean
                new_like, created = Post_Likes.objects.get_or_create(user=request.user, post=post)
        starGroupConvo = StarGroupConvo()

        dictionaryOfLikes = {}
        for groupConvo in ConvoPreview.objects.all():
            for postLike in Post_Likes.objects.all():
                if postLike.user == request.user and postLike.post == groupConvo:
                    dictionaryOfLikes[groupConvo.GroupId] = True
            if dictionaryOfLikes.get(groupConvo.GroupId) is None:
                dictionaryOfLikes[groupConvo.GroupId] = False

        favorites = []
        for postLike in Post_Likes.objects.all():
            if postLike.user == request.user:
                favorites.append(postLike)

        convoForm = NewConvoForm(request.POST)
        if convoForm.is_valid():
            Title = convoForm.cleaned_data['Group_Name']
            Description = convoForm.cleaned_data['Description']
            Thumbnail = convoForm.cleaned_data['Thumbnail']
            GroupId = ConvoPreview.objects.count()
            # args = {'Message': Message, 'Date': Date, 'Author': Author, 'Convo': Convo}
            NewConvo = ConvoPreview.objects.create(Group_Name = Title, Thumbnail = Thumbnail, Description = Description, GroupId = GroupId)
        convoForm = NewConvoForm()


        context = super(HomePage, self).get_context_data(*args,**kwargs)
        context['StarGroupConvo'] = starGroupConvo
        context['NewConvoForm'] = convoForm
        context['Post_Likes'] = Post_Likes.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['Dictionary'] = dictionaryOfLikes
        context['favorites'] = favorites
        return render(request, "./social_app/HomePage.html",context)
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

    def get_context_data(self, *args, **kwargs):
        for key, value in kwargs.items():
            GroupConvoID = value #since there is only one

        post = ConvoPreview.objects.get(GroupId=GroupConvoID)
        number_of_likes = Post_Likes.objects.filter(user=self.request.user, post=post).count()
        if number_of_likes > 0:
            already_liked = True # pass this variable to your context
        else:
            already_liked = False # you can make this anything other than boolean

        context = super(Messages, self).get_context_data(*args,**kwargs)
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['Post_Likes'] = Post_Likes.objects.all()
        postForm = NewPostForm()
        context['NewPostForm'] = postForm
        deleteForm = DeleteMessage()
        context['DeleteMessage'] = deleteForm
        starForm = StarGroupConvo()
        context['StarGroupConvo'] = starForm
        context['starred'] = already_liked
        return context


        # isMatch = False
        # for user in Post_Likes.objects.all():
        #     if user.user.id == request.user.id: #getting correct user
        #         for convo in user.starredGroupConvos:
        #             if convo.GroupId == val:   #getting correct ConvoPreview
        #                 isMatch = True
        #                 convoToRemove = convo
        #                 break
        #
        # print(slug_url_kwarg)

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

        starGroupConvo = StarGroupConvo(request.POST)
        if starGroupConvo.is_valid():
            post = ConvoPreview.objects.get(GroupId=GroupConvoID)
            number_of_likes = Post_Likes.objects.filter(user=request.user, post=post).count()
            if number_of_likes > 0:
                already_liked = True # pass this variable to your context
                Post_Likes.objects.filter(user=request.user, post=post).delete()
            else:
                already_liked = False # you can make this anything other than boolean
                new_like, created = Post_Likes.objects.get_or_create(user=request.user, post=post)
        starGroupConvo = StarGroupConvo()

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
        context['Post_Likes'] = Post_Likes.objects.all()
        context['NewPostForm'] = postForm
        context['DeleteMessage'] = deleteForm
        context['StarGroupConvo'] = starGroupConvo
        context['starred'] = not already_liked
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
            Post_Likes.objects.create(user = user)
            login(request, user)
            return redirect('../')
        else:
            signUpForm = SignUpForm()

        return render(request, './registration/registration.html', {'SignUpForm': signUpForm})
