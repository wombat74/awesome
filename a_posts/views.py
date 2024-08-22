from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .forms import *

def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    categories = Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'tag': tag
    }
    return render(request, 'a_posts/home.html', context)
@login_required
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

            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'a_posts/post_create.html', context)

@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)

    if request.method == 'POST':
        post.delete()

        messages.success(request, 'Post deleted...')
        return redirect('home')

    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_delete.html', context)

@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
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
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,
    }
    return render(request, 'a_posts/post_page.html', context)

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)

        if form.is_valid:
            print(f'Form was valid')
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    return redirect('post', post.id)

@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == 'POST':
        comment.delete()

        messages.success(request, 'Comment deleted...')
        return redirect('post', comment.parent_post.id)

    context = {
        'comment': comment,
    }
    return render(request, 'a_posts/comment_delete.html', context)

@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)

        if form.is_valid:
            print(f'Form was valid')
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    return redirect('post', comment.parent_post.id)

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()

        messages.success(request, 'Reply deleted...')
        return redirect('post', reply.parent_comment.parent_post.id)

    context = {
        'reply': reply,
    }
    return render(request, 'a_posts/reply_delete.html', context)

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exist = post.likes.filter(username=request.user.username).exists()

    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return redirect('post', post.id)