from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
  body = forms.CharField(
    label = '',
    widget = forms.Textarea(attrs={
      'rows': 2,
      'placeholder': 'Say Something...'
    })
  )
  class Meta:
    model = Post
    fields = ['body']

comment = forms.CharField(
    label = '',
    widget = forms.Textarea(attrs={
      'rows': 2,
      'placeholder': 'Comment on this Post!'
    })
  )