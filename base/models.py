from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
  body  = models.TextField()
  image = models.ImageField(upload_to='uploads/post_photos', null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  likes = models.ManyToManyField(User, related_name='likes', blank=True)
  dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
  created_on = models.DateTimeField(default=timezone.now)

  class Meta:
    ordering = ['-created_on']

  def __str__(self):
    return self.body
  

class Comment(models.Model):
  comment = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  likes = models.ManyToManyField(User,related_name='comment_likes', blank=True)
  dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
  created_on = models.DateTimeField(default=timezone.now)
  parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True)

  @property
  def children(self):
    return Comment.objects.filter(parent=self).order_by('-created_on')
  
  @property
  def is_parent(self):
    if self.parent is None:
      return True
    return False
  
  def __str__(self):
    return self.comment
  
class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
  name = models.CharField(max_length=100, null=True, blank=True)
  location = models.CharField(max_length=50, null=True, blank=True)
  bio = models.TextField(max_length=200, null=True, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/avatar.svg')
  followers = models.ManyToManyField(User, related_name='followers', blank=True)

  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()


class Notification(models.Model):
  notification_type = models.IntegerField()
  from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE)
  to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE)
  post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
  comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
  date = models.DateTimeField(default=timezone.now)
  user_has_seen = models.BooleanField(default=False)


class ThreadModel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class Message(models.Model):
  thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
  sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  body = models.CharField(max_length=1000)
  date = models.DateTimeField(default=timezone.now)
  is_read = models.BooleanField(default=False)