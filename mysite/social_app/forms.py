from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'email',)


class NewPostForm(forms.Form):
    Message = forms.CharField(label='Post Message')
    Date = forms.DateInput(attrs={'placeholder': '__/__/____', 'class': 'date',})
    Author = forms.CharField(label='Your name', max_length=100)
