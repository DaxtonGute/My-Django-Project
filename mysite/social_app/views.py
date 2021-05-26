from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import ConvoPreview, UserMessage, Post_Likes
# imports the forms that are stated in models.py
from .forms import NewPostForm, NewConvoForm, SignUpForm, DeleteMessage, StarGroupConvo, FilterBy
# imports the forms that are stated in forms.py
import datetime

class HomePage(TemplateView): # this controls everything on the home page
    template_name = "./social_app/HomePage.html" #template for the home page

    def get_context_data(self,*args, **kwargs): # this returns the context data when the user intially arrives
        context = super(HomePage, self).get_context_data(*args,**kwargs) # gets formatted context data for you to stuff context in
        if not self.request.user.is_anonymous: # checks if the user is logged in
            dictionaryOfLikes = {}
            # if they are then all of the posts that they have liked are compiled
            for groupConvo in ConvoPreview.objects.all():
                for postLike in Post_Likes.objects.all():
                    if postLike.user == self.request.user and postLike.post == groupConvo: # it has to be both the correct user and the correct group convo
                        dictionaryOfLikes[groupConvo.GroupId] = True
                if dictionaryOfLikes.get(groupConvo.GroupId) is None: # if there isn't a like for that post by the user then it is flagged that they didn't like it
                    dictionaryOfLikes[groupConvo.GroupId] = False
            context['Dictionary'] = dictionaryOfLikes.copy()

        favorites = [] # compiles all the posts the user has liked
        for postLike in Post_Likes.objects.all():
            if postLike.user == self.request.user:
                favorites.append(postLike) # it adds this like to favorites

        # loading the forms
        starGroupConvo = StarGroupConvo()
        context['StarGroupConvo'] = starGroupConvo
        convoForm = NewConvoForm()
        context['NewConvoForm'] = convoForm
        # loading the rest of the context
        context['favorites'] = favorites
        context['ConvoPreview'] = ConvoPreview.objects.all()
        if len(favorites) != 0: # if the user doesn't have any favorites, then the favorites won't appear
            context['hasFavorites'] = True
        else:
            context['hasFavorites'] = False
        # preloads the filter buttons to false
        context['byRecent'] = False
        context['byHot'] = False
        context['byLikes'] = False
        return context

    def post(self, request, *args, **kwargs): # this returns the context data when the user interacts with the page
        context = super(HomePage, self).get_context_data(*args,**kwargs) # gets formatted context data for you to stuff context in

        # this is if a user clicks the like button
        starGroupConvo = StarGroupConvo(request.POST)
        if not self.request.user.is_anonymous:
            if starGroupConvo.is_valid() and starGroupConvo.cleaned_data['star'] != "":
                GroupConvoID = starGroupConvo.cleaned_data['star']
                post = ConvoPreview.objects.get(GroupId=GroupConvoID)
                number_of_likes = Post_Likes.objects.filter(user=request.user, post=post).count() # checks how many likes the user currently has on that post
                if number_of_likes > 0: # changes the button's state and adds or deletes that post like depending on current state
                    already_liked = True
                    Post_Likes.objects.filter(user=request.user, post=post).delete()
                else:
                    already_liked = False
                    new_like, created = Post_Likes.objects.get_or_create(user=request.user, post=post)
            starGroupConvo = StarGroupConvo()

        # this is if a user clicks the new convo button
        convoForm = NewConvoForm(request.POST, request.FILES)
        if convoForm.is_valid():
            Title = convoForm.cleaned_data['Title']
            Description = convoForm.cleaned_data['Description']
            Thumbnail = convoForm.cleaned_data['Thumbnail']
            GroupId = ConvoPreview.objects.count()
            Date = datetime.datetime.today()
            # it creates a new convo
            NewConvo = ConvoPreview.objects.create(Group_Name = Title, Thumbnail = Thumbnail, Description = Description, GroupId = GroupId, Time_Stamp = Date)
        convoForm = NewConvoForm()

        if not self.request.user.is_anonymous: # checks if the user is logged in
            dictionaryOfLikes = {}
            # if they are then all of the posts that they have liked are compiled
            for groupConvo in ConvoPreview.objects.all():
                for postLike in Post_Likes.objects.all():
                    if postLike.user == self.request.user and postLike.post == groupConvo: # it has to be both the correct user and the correct group convo
                        dictionaryOfLikes[groupConvo.GroupId] = True
                if dictionaryOfLikes.get(groupConvo.GroupId) is None: # if there isn't a like for that post by the user then it is flagged that they didn't like it
                    dictionaryOfLikes[groupConvo.GroupId] = False
            context['Dictionary'] = dictionaryOfLikes.copy()

        favorites = [] # compiles all the posts the user has liked
        for postLike in Post_Likes.objects.all():
            if postLike.user == self.request.user:
                favorites.append(postLike) # it adds this like to favorites

        # presets all of the buttons to false so that things will only sort if you click on them
        byRecent = False
        byHot = False
        byLikes = False
        RequestedConvos = ConvoPreview.objects.all()
        filterBy = FilterBy(request.POST)
        if filterBy.is_valid():
            #checks which type of sort they want to use
            if filterBy.cleaned_data['filter'] == 'byRecent':
                byRecent = not bool(filterBy.cleaned_data['active'])
                RequestedConvos = ConvoPreview.objects.all().order_by('-Time_Stamp') # sorts by reverse chronological order

            elif filterBy.cleaned_data['filter'] == 'byHot':
                byHot = not bool(filterBy.cleaned_data['active'])
                RequestedConvos = sorted(ConvoPreview.objects.all(), key=lambda m: -m.hotness) # sorts by that hotness algorithm

            elif filterBy.cleaned_data['filter'] == 'byLikes':
                byLikes = not bool(filterBy.cleaned_data['active'])
                RequestedConvos = sorted(ConvoPreview.objects.all(),  key=lambda m: -m.view_count) # sorts by likes

        # passes in form context
        context['StarGroupConvo'] = starGroupConvo
        context['NewConvoForm'] = convoForm
        context['Post_Likes'] = Post_Likes.objects.all()
        context['ConvoPreview'] = RequestedConvos
        context['favorites'] = favorites
        if len(favorites) != 0: # passes in if they have favorites
            context['hasFavorites'] = True
        else:
            context['hasFavorites'] = False
        # passes in button context
        context['byRecent'] = byRecent
        context['byHot'] = byHot
        context['byLikes'] = byLikes
        return render(request, "./social_app/HomePage.html",context)

class Messages(TemplateView):
    template_name = "./social_app/Messages.html"
    slug_url_kwarg = 'GroupConvoID'

    def get_context_data(self, *args, **kwargs): # this returns the context data when the user intially arrives
        context = super(Messages, self).get_context_data(*args,**kwargs) # gets formatted context data for you to stuff context in
        for key, value in kwargs.items():
            GroupConvoID = value # since there is only one

        if not self.request.user.is_anonymous:
            post = ConvoPreview.objects.get(GroupId=GroupConvoID)
            number_of_likes = Post_Likes.objects.filter(user=self.request.user, post=post).count() # checks how many likes the user currently has on that post
            if number_of_likes > 0: # changes the button's state and adds or deletes that post like depending on current state
                already_liked = True
            else:
                already_liked = False
            context['starred'] = already_liked

        # passes in form context
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

    def post(self, request, *args, **kwargs): # this returns the context data when the user interacts with the page
        context = super(Messages, self).get_context_data(*args,**kwargs) # gets formatted context data for you to stuff context in
        for key, value in kwargs.items():
            GroupConvoID = value #since there is only one

        # form for deleting a message
        deleteForm = DeleteMessage(request.POST)
        if deleteForm.is_valid():
            val = deleteForm.cleaned_data.get("deleteBtn")
            for message in UserMessage.objects.all():
                if str(message) == str(val):
                    message.delete() # deletes the message
        deleteForm = DeleteMessage()

        # checks likes for this user and this convo preview
        if not self.request.user.is_anonymous:
            starGroupConvo = StarGroupConvo(request.POST)
            if starGroupConvo.is_valid():
                post = ConvoPreview.objects.get(GroupId=GroupConvoID)
                number_of_likes = Post_Likes.objects.filter(user=request.user, post=post).count() # checks how many likes the user currently has on that post
                if number_of_likes > 0: # changes the button's state and adds or deletes that post like depending on current state
                    already_liked = True
                    Post_Likes.objects.filter(user=request.user, post=post).delete()
                else:
                    already_liked = False
                    new_like, created = Post_Likes.objects.get_or_create(user=request.user, post=post)
            starGroupConvo = StarGroupConvo()
            context['starred'] = not already_liked

        # form for creating a new post
        postForm = NewPostForm(request.POST)
        if postForm.is_valid():
            Message = postForm.cleaned_data['Message']
            Author = request.user
            Date = datetime.datetime.today()
            postForm = NewPostForm()
            for Convo in ConvoPreview.objects.all():
                 if str(Convo.GroupId) == GroupConvoID:
                    NewMessage = UserMessage.objects.create(Message_Text = Message, Time_Stamp = Date, Author = Author, GroupConvo = Convo) # creates a new post
        postForm = NewPostForm()

        #passes in context
        context['UserMessage'] = UserMessage.objects.all()
        context['ConvoPreview'] = ConvoPreview.objects.all()
        context['Post_Likes'] = Post_Likes.objects.all()
        context['NewPostForm'] = postForm
        context['DeleteMessage'] = deleteForm
        context['StarGroupConvo'] = starGroupConvo
        return render(request, "./social_app/Messages.html",context)

class registration(TemplateView):
    template_name = "./registration/registration.html"

    def get_context_data(self,*args, **kwargs): # this returns the context data when the user intially arrives
        context = super(registration, self).get_context_data(*args,**kwargs) # gets formatted context data for you to stuff context in
        # gives the registration form context
        signUpForm = SignUpForm()
        context['SignUpForm'] = signUpForm
        return context

    def post(self, request, *args, **kwargs): # this returns the context data when the user interacts with the page

        # its the default registration form
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
            login(request, user) # logs the user in
            return redirect('../') # returns the user back to the main page
        else:
            signUpForm = SignUpForm()

        return render(request, './registration/registration.html', {'SignUpForm': signUpForm})
