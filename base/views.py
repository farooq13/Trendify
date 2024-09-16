from django.shortcuts import render
from django.views import View

  
class PostList(View):
  def get(self, request, *args, **kwargs):

    context = {}
    return render(request, 'base/post_list.html', context)
