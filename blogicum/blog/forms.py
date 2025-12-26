from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comments


User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)
