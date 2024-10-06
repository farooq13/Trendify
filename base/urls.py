from django.urls import path
from .views import PostList, PostDetail, PostEdit, PostDelete, CommentReply, CommentDelete, CommentEdit, Profile, ProfileEdit, AddFollower, RemoveFollower, UserSearch, PostLike, PostDislike, CommentLike, CommentDislike, PostNotification, FollowNotification, RemoveNotification


urlpatterns = [
  path('', PostList.as_view(), name='home'),
  path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
  path('post/edit/<pk>/', PostEdit.as_view(), name='post-edit'),
  path('post/delete/<int:pk>/', PostDelete.as_view(), name='post-delete'),
  path('post/<int:pk>/likes/', PostLike.as_view(), name='post-like'),
  path('post/<int:pk>/dislikes/', PostDislike.as_view(), name='post-dislike'),
  
  path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReply.as_view(), name='comment-reply'),
  path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment-delete'),
  path('post/<int:post_pk>/comment/edit/<int:pk>/', CommentEdit.as_view(), name='comment-edit'),
  path('post/<int:post_pk>/comment/<int:pk>/likes', CommentLike.as_view(), name='comment-like'),
  path('post/<int:post_pk>/comment/<int:pk>/dislikes', CommentDislike.as_view(), name='comment-dislike'),

  path('profile/<int:pk>/', Profile.as_view(), name='profile'),
  path('profile/<int:pk>/edit/', ProfileEdit.as_view(), name='profile-edit'),
  path('profile/<int:pk>/followers/add/', AddFollower.as_view(), name='follow'),
  path('profile/<int:pk>/followers/remove/', RemoveFollower.as_view(), name='unfollow'),

  path('search/', UserSearch.as_view(), name='user-search'),

  path('notification/<int:notification_pk>/post/<int:post_pk>/', PostNotification.as_view(), name='post-notification'),
  path('notification/<int:notification_pk>/profile/<int:profile_pk>/', FollowNotification.as_view(), name='follow-notification'),
  path('notification/<int:notification_pk>/', RemoveNotification.as_view(), name='notification-remove'),
]