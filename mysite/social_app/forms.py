from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2',)


class NewPostForm(forms.Form):
    Message = forms.CharField(label='Post Message')
    
