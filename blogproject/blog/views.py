from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown

# Create your views here.

# from django.http import HttpResponse


def index(request):
    # return HttpResponse("liang shao dong huan ying nin !")
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html',
                  context={'title': 'this is a title', 'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  entensions=['markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',])
    return render(request, 'blog/detail.html', context={'post': post})
