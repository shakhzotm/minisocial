from django import forms
from .models import Profile, Post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'city', 'birth_date', 'avatar']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description']
