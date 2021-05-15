from django import forms
from django.contrib.auth.models import User
from .models import ConvoPreview
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2',)


class NewPostForm(forms.Form):
    Message = forms.CharField(label='Post Message')

class NewConvoForm(forms.Form): #use .ModelForm for models
    # class Meta:
    #     model = ConvoPreview
    #     fields = [
    #     'Group_Name',
    #     'Description',
    #     'Thumbnail',
    #     ]
    Title = forms.CharField(label='Title')
    Description = forms.CharField(label='Description')
    Thumbnail = forms.ImageField(label='Thumbnail')

class DeleteMessage(forms.Form):
     deleteBtn = forms.CharField(required = False)

class StarGroupConvo(forms.Form):
     star = forms.CharField(required = False)

class FilterBy(forms.Form):
     star = forms.CharField(required = False)
