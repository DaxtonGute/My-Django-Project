from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import ConvoPreview, UserMessage, Post_Likes
from .forms import NewPostForm, NewConvoForm, SignUpForm, DeleteMessage, StarGroupConvo, FilterBy
import datetime

class HomePage(TemplateView):
    template_name = "./social_app/HomePage.html"
    model = ConvoPreview

    def get_context_data(self,*args, **kwargs):
        context = super(HomePage, self).get_context_data(*args,**kwargs)
        if not self.request.user.is_anonymous:
            dictionaryOfLikes = {}
            for groupConvo in ConvoPreview.objects.all():
                for postLike in Post_Likes.objects.all():
                    if postLike.user == self.request.user and postLike.post == groupConvo:
                        dictionaryOfLikes[groupConvo.GroupId] = True
                if dictionaryOfLikes.get(groupConvo.GroupId) is None:
                    dictionaryOfLikes[groupConvo.GroupId] = False
            context['Dictionary'] = dictionaryOfLikes.copy()

        favorites = []
        for postLike in Post_Likes.objects.all():
            if postLike.user == self.request.user:
                favorites.append(postLike)

        starGroupConvo = StarGroupConvo()
        context['StarGroupConvo'] = starGroupConvo
        convoForm = NewConvoForm()
        context['NewConvoForm'] = convoForm
        context['favorites'] = favorites
        context['ConvoPreview'] = ConvoPreview.objects.all()
        if len(favorites) != 0:
            context['hasFavorites'] = True
        else:
            context['hasFavorites'] = False
        context['byRecent'] = False
        context['byHot'] = False
        context['byLikes'] = False
        return context

    def post(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args,**kwargs)
        starGroupConvo = StarGroupConvo(request.POST)
        if not self.request.user.is_anonymous:
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

        convoForm = NewConvoForm(request.POST, request.FILES)
        if convoForm.is_valid():
            Title = convoForm.cleaned_data['Title']
            Description = convoForm.cleaned_data['Description']
            Thumbnail = convoForm.cleaned_data['Thumbnail']
            GroupId = ConvoPreview.objects.count()
            Date = datetime.datetime.today()
            # args = {'Message': Message, 'Date': Date, 'Author': Author, 'Convo': Convo}
            NewConvo = ConvoPreview.objects.create(Group_Name = Title, Thumbnail = Thumbnail, Description = Description, GroupId = GroupId, Time_Stamp = Date)
        convoForm = NewConvoForm()


        if not self.request.user.is_anonymous:
            dictionaryOfLikes = {}
            for groupConvo in ConvoPreview.objects.all():
                for postLike in Post_Likes.objects.all():
                    if postLike.user == request.user and postLike.post == groupConvo:
                        dictionaryOfLikes[groupConvo.GroupId] = True
                if dictionaryOfLikes.get(groupConvo.GroupId) is None:
                    dictionaryOfLikes[groupConvo.GroupId] = False
            context['Dictionary'] = dictionaryOfLikes

        favorites = []
        for postLike in Post_Likes.objects.all():
            if postLike.user == request.user:
                favorites.append(postLike)

        byRecent = False
        byHot = False
        byLikes = False
        RequestedConvos = ConvoPreview.objects.all()
        filterBy = FilterBy(request.POST)
        if filterBy.is_valid():
            print(filterBy.cleaned_data['active'])
            if filterBy.cleaned_data['filter'] == 'byRecent':
                byRecent = not bool(filterBy.cleaned_data['active'])
                RequestedConvos = ConvoPreview.objects.all().order_by('-Time_Stamp')

            elif filterBy.cleaned_data['filter'] == 'byHot':
                byHot = not bool(filterBy.cleaned_data['active'])
                RequestedConvos = sorted(ConvoPreview.objects.all().order_by('-Time_Stamp'), key=lambda m: m.hotness)
                
            elif filterBy.cleaned_data['filter'] == 'byLikes':
                byLikes = not bool(filterBy.cleaned_data['active'])
                RequestedConvos = sorted(ConvoPreview.objects.all(),  key=lambda m: m.view_count)


        context['StarGroupConvo'] = starGroupConvo
        context['NewConvoForm'] = convoForm
        context['Post_Likes'] = Post_Likes.objects.all()
        context['ConvoPreview'] = RequestedConvos
        context['favorites'] = favorites
        if len(favorites) != 0:
            context['hasFavorites'] = True
        else:
            context['hasFavorites'] = False

        context['byRecent'] = byRecent
        context['byHot'] = byHot
        context['byLikes'] = byLikes
        return render(request, "./social_app/HomePage.html",context)

class Messages(TemplateView):
    template_name = "./social_app/Messages.html"
    model = UserMessage
    slug_url_kwarg = 'GroupConvoID'

    def get_context_data(self, *args, **kwargs):
        context = super(Messages, self).get_context_data(*args,**kwargs)
        for key, value in kwargs.items():
            GroupConvoID = value #since there is only one
        if not self.request.user.is_anonymous:
            post = ConvoPreview.objects.get(GroupId=GroupConvoID)
            number_of_likes = Post_Likes.objects.filter(user=self.request.user, post=post).count()
            if number_of_likes > 0:
                already_liked = True # pass this variable to your context
            else:
                already_liked = False # you can make this anything other than boolean
            context['starred'] = already_liked

        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['Post_Likes'] = Post_Likes.objects.all()
        postForm = NewPostForm()
        context['NewPostForm'] = postForm
        deleteForm = DeleteMessage()
        context['DeleteMessage'] = deleteForm
        starForm = StarGroupConvo()
        context['StarGroupConvo'] = starForm
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
        context = super(Messages, self).get_context_data(*args,**kwargs)
        for key, value in kwargs.items():
            GroupConvoID = value #since there is only one

        deleteForm = DeleteMessage(request.POST)
        if deleteForm.is_valid():
            val = deleteForm.cleaned_data.get("deleteBtn")
            for message in UserMessage.objects.all():
                if str(message) == str(val):
                    message.delete()
        deleteForm = DeleteMessage()

        if not self.request.user.is_anonymous:
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
            context['starred'] = not already_liked

        postForm = NewPostForm(request.POST)
        if postForm.is_valid():
            Message = postForm.cleaned_data['Message']
            Author = request.user
            Date = datetime.datetime.today()
            postForm = NewPostForm()
            # args = {'Message': Message, 'Date': Date, 'Author': Author, 'Convo': Convo}
            for Convo in ConvoPreview.objects.all():
                 if str(Convo.GroupId) == GroupConvoID:
                    NewMessage = UserMessage.objects.create(Message_Text = Message, Time_Stamp = Date, Author = Author, GroupConvo = Convo)
        postForm = NewPostForm()

        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['Post_Likes'] = Post_Likes.objects.all()
        context['NewPostForm'] = postForm
        context['DeleteMessage'] = deleteForm
        context['StarGroupConvo'] = starGroupConvo
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
            login(request, user)
            return redirect('../')
        else:
            signUpForm = SignUpForm()

        return render(request, './registration/registration.html', {'SignUpForm': signUpForm})
