from django import forms
from django.contrib.auth.models import User

from .models import Profile, Post, PostComment, PostLike, CommentLike

class UserForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'img']

class PostCommentForm(forms.ModelForm):
    description = forms.CharField(max_length=500)
    class Meta:
        model = PostComment
        fields = ['description']