from django.forms import ModelForm
from .models import Post, Comment, UserProfile


class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ['body', 'image']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']

class ProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    fields = ['picture', 'name', 'bio', 'location', 'birth_date']