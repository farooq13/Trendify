from django.urls import path
from .views import PostList, PostDetail, PostEdit, PostDelete, CommentReply, CommentDelete, CommentEdit


urlpatterns = [
  path('', PostList.as_view(), name='home'),
  path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
  path('post/edit/<pk>/', PostEdit.as_view(), name='post-edit'),
  path('post/delete/<int:pk>/', PostDelete.as_view(), name='post-delete'),
  
  path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReply.as_view(), name='comment-reply'),
  path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment-delete'),
  path('post/<int:post_pk>/comment/edit/<int:pk>/', CommentEdit.as_view(), name='comment-edit'),
]