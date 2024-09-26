from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, UserProfile
from django.db.models import Q
from .forms import PostForm, CommentForm, ProfileForm

  
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
  def get(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    comments = Comment.objects.filter(post=post)
    
    context = {
      'post': post,
      'form': form,
      'comments': comments
    }
    return render(request, 'base/post_detail.html', context)
  
  def post(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
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
    pk = self.kwargs['pk']
    return reverse_lazy('post-detail', kwargs={'pk':pk})
  
  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
  

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'base/post_delete.html'
  success_url = reverse_lazy('home')
  

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
  

class CommentReply(LoginRequiredMixin, View):
  def post(self, request, post_pk, pk, *args, **kwargs):
    post = Post.objects.get(pk=post_pk)
    parent_comment = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
      new_comment = form.save(commit=False)
      new_comment.post = post
      new_comment.parent = parent_comment
      new_comment.author = request.user
      new_comment.save()
      
      return redirect('post-detail', pk=post_pk)
  
class CommentEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Comment
  fields = ['comment']
  template_name = 'base/comment_edit.html'

  def get_success_url(self):
    post_pk = self.kwargs['post_pk']
    return reverse_lazy('post-detail', kwargs={'pk':post_pk})
  
  def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  template_name = 'base/comment_delete.html'

  def get_success_url(self):
    post_pk = self.kwargs['post_pk']
    return reverse_lazy('post-detail', kwargs={'pk': post_pk})
  

class Profile(View):
  def get(self, request, pk, *args, **kwargs):
    profile = get_object_or_404(UserProfile, pk=pk)
    user = profile.user
    posts = Post.objects.filter(author=user).all()
    form = ProfileForm(request.POST, request.FILES)
    context = {
      'profile': profile,
      'user': user,
      'posts': posts,
      'form': form
    }

    return render(request,'base/profile.html', context)
  
class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = UserProfile
  fields = ['picture', 'name', 'bio', 'location', 'birth_date']
  template_name = 'base/profile_edit.html'

  def get_success_url(self):
    pk = self.kwargs['pk']
    return reverse_lazy('profile', kwargs={'pk':pk})
  
  def test_func(self):
    profile = self.get_object()
    return self.request.user == profile.user