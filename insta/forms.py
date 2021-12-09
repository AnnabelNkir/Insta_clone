from django import forms
from .models import Image,Profile, Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['likes','profile','posted_time','profile','user']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['image','user']

class EditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_pic']