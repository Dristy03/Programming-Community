from django import forms
from django.contrib.auth import models
from django.db.models import fields

from post.models import Post,Comment

# creates the form for creating post
class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['text']

# creates the form for comment
class CommentForm(forms.ModelForm):
	body = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        
    }))
	class Meta:
		model = Comment
		fields = ['body','comment_image']

