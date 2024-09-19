from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
  body  = models.TextField()
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
  user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile', verbose_name='user')
  name = models.CharField(max_length=200)
  location = models.CharField(max_length=100, null=True, blank=True)
  bio = models.TextField(null=True, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/avatar.svg')
  followers = models.ManyToManyField(User, related_name='followers', null=True, blank=True)

  def __str__(self):
    return self.name
  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, *args, **kwargs):
  instance.profile.save()
