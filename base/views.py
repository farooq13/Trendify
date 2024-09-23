from django.shortcuts import render
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, UserProfile
from django.db.models import Q
from .forms import PostForm, CommentForm

  
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
    return render(request, 'base/index.html', context)
  
  def post(self, request, *args, **kwargs):
    posts = Post.objects.filter(
      Q(author__profile__followers__in=[request.user.id]) |
      Q(author=request.user)
    )
    form = PostForm(request.POST)

    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()

    context = {
      'posts': posts,
      'form': form
    }
    return render(request, 'base/index.html', context)
  

class PostDetail(View, LoginRequiredMixin):
  def get(self, request, post_id, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post=post)
    
    context = {
      'post': post,
      'form': form,
      'comments': comments
    }
    return render(request, 'base/post_detail.html', context)
  
  def post(self, request, post_id, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.author = request.user
      comment.post = post
      comment.save()

    context = {
      'post': post,
      'form': form
    }
    return render(request, 'base/post_detail.html', context)
  
class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  template_name = 'base/post_edit.html'
  fields = ['body']

  def get_success_url(self):
    id = self.kwargs['id']
    return reverse_lazy('post-detail', kwargs={'id':id})
  
  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
  

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'base/delete_post.html'
  success_url = reverse_lazy('home')

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author