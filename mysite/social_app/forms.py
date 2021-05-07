from django import forms
from django.contrib.auth.models import User
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

class NewConvoForm(forms.Form):
    Title = forms.CharField(label='Title')
    Description = forms.CharField(label='Description')
    Thumbnail = forms.ImageField(label='Thumbnail')

class DeleteMessage(forms.Form):
     deleteBtn = forms.CharField(required = False)

class StarGroupConvo(forms.Form):
     star = forms.CharField(required = False)
