from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from . models import *
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.forms import AuthenticationForm

class AuthForm(AuthenticationForm):
    pass
class Signup(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "First name"}), max_length=20, required=True, help_text="Please enter your first name")
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Last name"}), max_length=20, required=True, help_text="Please enter your last name")
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"placeholder": "Email"}),max_length=200, required=True, help_text="Please enter a valid email address")

    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Select a username"}), max_length=12, min_length=4, help_text="Please your phone number")

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Choose an 8 Character long password"
    }), label="Enter password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm your password"
    }), label="Enter password")


    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2", "email"]


class UserDetailForm(forms.Form):
    user = forms.CharField()
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Phone"}), max_length=12, min_length=11, help_text="Please your phone number")
    dob = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}),
                            required=True)
    dp = forms.FileField()
    country = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Country"}), max_length=20, min_length=2, help_text="Please select your country")
    stateRegion = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "State/Region"}), max_length=12, min_length=11, help_text="Please your phone number")
    sex = forms.CharField()

    class Meta:
        model = Users
        fields = ["phone", "dob","country", "dp", "stateRegion", "sex", "user"]


class PostCreationForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Create post"}))
    pic = forms.FileField()

    class Meta:
        model = Posts
        fields = ["content", "post"]


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Comment"}))
    post = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Comment
        fields = ["comment", "post"]


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Ask Me"}))

class LikeForm(forms.Form):
    post = forms.IntegerField()

    class Meta:
        model = Like
        fields =["post"]