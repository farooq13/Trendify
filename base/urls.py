from django.urls import path
from .views import PostList, PostDetail, PostEdit, PostDelete, CommentReply, CommentDelete, CommentEdit, Profile, ProfileEdit, AddFollower, RemoveFollower, UserSearch


urlpatterns = [
  path('', PostList.as_view(), name='home'),
  path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
  path('post/edit/<pk>/', PostEdit.as_view(), name='post-edit'),
  path('post/delete/<int:pk>/', PostDelete.as_view(), name='post-delete'),
  
  path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReply.as_view(), name='comment-reply'),
  path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment-delete'),
  path('post/<int:post_pk>/comment/edit/<int:pk>/', CommentEdit.as_view(), name='comment-edit'),

  path('profile/<int:pk>/', Profile.as_view(), name='profile'),
  path('profile/<int:pk>/edit/', ProfileEdit.as_view(), name='profile-edit'),
  path('profile/<int:pk>/followers/add/', AddFollower.as_view(), name='follow'),
  path('profile/<int:pk>/followers/remove/', RemoveFollower.as_view(), name='unfollow'),

  path('search/', UserSearch.as_view(), name='user-search'),
]