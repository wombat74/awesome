from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .forms import *

def home_view(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, 'a_posts/home.html', context)

def post_create_view(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')

            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            # looks like: <meta content="https://live.staticflickr.com/65535/51964172707_38fd9f1e06_b.jpg">

            image = find_image[0]['content'] # access url related to the 'content' meta attribute
            post.image = image

            find_title = sourcecode.select('h1.photo-title') # grab the h1 element with the class 'photo-title'
            title = find_title[0].text.strip() # grab 1st element in list turn it to text and strip any white-space
            post.title = title

            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist

            post.save()
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'a_posts/post_create.html', context)

def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        post.delete()

        messages.success(request, 'Post deleted...')
        return redirect('home')

    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_delete.html', context)

def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post) # takes the current instance an populates the form
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('home')

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'a_posts/post_edit.html', context)

def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_page.html', context)