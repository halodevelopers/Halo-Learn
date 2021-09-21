from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    #  Post.objects.filter(status='published')
    posts = Post.published.all()
    
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not the first page, deliver an intger
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page
        posts = paginator.page(paginator.num_page)
    
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