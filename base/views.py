from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, UserProfile, Notification
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
    form = PostForm(request.POST, request.FILES)

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
      'comments': comments,
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

    notification = Notification.objects.create(
      notification_type = 2,
      from_user = request.user,
      to_user = post.author,
      post=post
    )

    context = {
      'post': post,
      'form': form
    }
    return render(request, 'base/post_detail.html', context)
  
class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  template_name = 'base/post_edit.html'
  fields = ['body', 'image']

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
  

class PostLike(LoginRequiredMixin, View):
  def post (self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.likes.all():
      post.likes.remove(user)
    if user in post.dislikes.all():
      post.dislikes.remove(request.user)
      post.likes.add(user)

      notification = Notification.objects.create(
        notification_type = 1,
        from_user = request.user,
        to_user = post.author,
        post = post
      )

    next = request.POST.get('next')
    return HttpResponseRedirect(next)
  
class PostDislike(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.dislikes.all():
      post.dislikes.remove(user)
    if user in post.likes.all():
      post.likes.remove(user)
      post.dislikes.add(user)

    next = request.POST.get('next')
    return HttpResponseRedirect(next)

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

      notification = Notification.objects.create(
        notification_type = 2,
        from_user = new_comment.author,
        to_user = parent_comment.author,
        comment = parent_comment
      )
      
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

class CommentLike(LoginRequiredMixin, View):
  def post(self, request,post_pk, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if user in comment.likes.all():
      comment.likes.remove(user)
    if user in comment.dislikes.all():
      comment.dislikes.remove(user)
      comment.likes.add(user)

      notification = Notification.objects.create(
        notification_type = 1,
        from_user = request.user,
        to_user = comment.author,
        comment = comment
      )

    next = request.POST.get('next')
    return HttpResponseRedirect(next)

class CommentDislike(LoginRequiredMixin, View):
  def post(self, request,post_pk, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if user in comment.dislikes.all():
      comment.dislikes.remove(user)
    if user in comment.likes.all():
      comment.likes.remove(user)
      comment.dislikes.add(user)
    
    next = request.POST.get('next')
    return HttpResponseRedirect(next)


class Profile(View):
  def get(self, request, pk, *args, **kwargs):
    profile = UserProfile.objects.get(pk=pk)
    user = profile.user
    posts = Post.objects.filter(author=user)
    followers = profile.followers.all()
    num_of_followers = len(followers)

    is_following = False
    for follower in followers:
      if follower == request.user:
        is_following = True
      else:
        is_following = False

    context = {
      'profile': profile, 
      'user': user, 'posts': posts, 
      'followers': followers, 
      'num_of_followers': num_of_followers, 
      'is_following': is_following
      }
    return render(request, 'base/profile.html', context)
  
class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = UserProfile
  fields = ['picture', 'name', 'location', 'birth_date', 'bio']
  template_name = 'base/profile_edit.html'

  def get_success_url(self):
    pk = self.kwargs['pk']
    return reverse_lazy('profile', kwargs={'pk': pk})
  
  def test_func(self):
    profile = self.get_object()
    return self.request.user == profile.user
  
class AddFollower(View):
  def post(self, request, pk, *args, **kwargs):
    profile = UserProfile.objects.get(pk=pk)
    profile.followers.add(request.user)

    notification = Notification.objects.create(
      notification_type = 3,
      from_user = request.user,
      to_user = profile.user
    )

    return redirect('profile', pk=profile.pk)
  
class RemoveFollower(View):
  def post(self, request, pk, *args, **kwargs):
    profile = UserProfile.objects.get(pk=pk)
    profile.followers.remove(request.user)

    return redirect('profile', pk=profile.pk)
  

class UserSearch(View):
  def get(self, request,*args, **kwargs):
    query = request.GET.get('query')
    profile_list = UserProfile.objects.filter(
      Q(user__username__icontains=query)
    )
    
    context = {
      'query': query,
      'profile_list': profile_list
    }

    return render(request, 'base/search.html', context)
  


class PostNotification(View):
  def get(self, request, notification_pk, post_pk, *args, **kwargs):
    notification = Notification.objects.get(pk=notification_pk)
    post = Post.objects.get(pk=post_pk)

    notification.user_has_seen = True
    notification.save()
    return redirect('post-detail', pk=post_pk)
  

class FollowNotification(View):
  def get(self, request, notification_pk, profile_pk, *args, **kwargs):
    notification = Notification.objects.get(pk=notification_pk)
    profile = UserProfile.objects.get(pk=profile_pk)

    notification.user_has_seen = True
    notification.save()
    return redirect('profile', pk=profile.pk)
  
class RemoveNotification(View):
  def delete(self, request, notification_pk, *args, **kwargs):
    notification = Notification.objects.get(pk=notification_pk)
    notification.user_has_seen = True
    notification.save()
    return HttpResponse('success', content_type='text/plain')