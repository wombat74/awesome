from django.shortcuts import render
from .models import *

def home_view(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'a_posts/home.html', context)

def post_create_view(request):
    return render(request, 'a_posts/post_create.html')
