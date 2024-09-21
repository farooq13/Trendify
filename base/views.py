from django.shortcuts import render
from django.views import View
from .models import Post, Comment, UserProfile
from django.db.models import Q
from .forms import PostForm

  
class PostList(View):
  def get(self, request, *args, **kwargs):
    posts = Post.objects.filter(
      Q(author__profile__followers__in=[request.user.id]) |
      Q(author=request.user)
    )
    form = PostForm()
    
    context = {
      'posts': posts,
      'form': form
    }
    return render(request, 'base/post_list.html', context)
  
  def post(self, request, *args, **kwargs):
    posts = Post.objects.filter(
      Q(author__profile__followers__in=[request.user.id]) |
      Q(author=request.user)
    )
    form = PostForm(request.POST)

    context = {
      'posts': posts,
      'form': form
    }
    return render(request, 'base/post_list.html', context)
