from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms

class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'name',
            'bio',
            'email',
            'profile_image',
            'social_instagram',
            'social_twitter',
            'social_youtube',
        ]

class RegisterUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"input",
            "type": "text",
            "placeholder" :"Your Username"
        }
    ), label="")
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"input",
            "type": "email",
            "placeholder" :"Your Email"
        }
    ), label="")
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"input",
            "type": "password",
            "placeholder" :"Password"
        }
    ), label="")
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"input",
            "type": "password",
            "placeholder" :"Repeat your password"
        }
    ), label="")

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]