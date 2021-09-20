from django.shortcuts import get_object_or_404, render
from .models import Post
# Create your views here.
def post_list(request):
    #  Post.objects.filter(status='published')
    posts = Post.published.all()
    context = {
        "posts": posts
    }
    return render(request, "post_list.html", {'posts':posts})


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    context = {
        'post': post
    }
    
    return render(request, 'post_detail.html', {'post':post})