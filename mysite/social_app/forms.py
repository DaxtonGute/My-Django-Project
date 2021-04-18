from django import forms


class NewPostForm(forms.Form):
    Message = forms.CharField(label='Post Message')
    Date = forms.DateInput(attrs={'placeholder': '__/__/____', 'class': 'date',})
    Author = forms.CharField(label='Your name', max_length=100)
