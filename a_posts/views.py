from django.shortcuts import render, redirect
from .models import *
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
import requests

def home_view(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, 'a_posts/home.html', context)

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body']
        labels = {
            'body': 'Caption',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption...', 'class': 'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder': 'Add url...'}),
        }

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
