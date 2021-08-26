from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.db.models import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, widgets
from django.core.paginator import Paginator
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, Like

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': widgets.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Say Something",
                'style': "width: 87%;"
            })
        }
        labels = {
            'content': ""
        }

def index(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.timestamp = datetime.now()
            form.save()
    return render(request, "network/index.html", {
        "form": NewPostForm()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user(request,username):
    print(f"username: {username}")
    profile = User.objects.filter(username=username).first()
    posts = Post.objects.filter(author=profile)
    following = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(user=request.user,following=profile)
        if follow:
            following = True

    if request.method == "POST":
        if not following:
            follow = Follow(user=request.user,following=profile)
            follow.save()
            following = True
        else:
            follow.delete()
            following = False

    num_followers = Follow.objects.filter(following=profile).count()
    num_following = Follow.objects.filter(user=profile).count()
    return render(request,"network/user.html",{
        "profile": profile,
        "posts": posts,
        "is_following": following,
        "followers": num_followers,
        "following": num_following
    })

@login_required
def following(request):
    follows = Follow.objects.filter(user=request.user)
    following = []
    for follow in follows:
        following.append(getattr(follow,"following").username)
    posts = Post.objects.filter(author__username__in=following).order_by('-pk')
    return render(request,"network/following.html", {
        "posts": posts
    })

def posts(request):
    # Get all posts in reverse order
    count = Post.objects.all().count()
    data = []
    user = ""
    for i in range(count):
        post = Post.objects.all()[count-i-1:count-i].get()

        if request.user.is_authenticated:
            # Check if current user has liked the post
            liked = Like.objects.filter(user=request.user,post=post)
            user = request.user.username
            if liked:
                liked = True
            else:
                liked = False
            data.append([post.author.username,post.content,post.timestamp.strftime("%H:%M:%S • %m/%d/%Y"),post.num_likes,liked,post.pk])
        else:
            data.append([post.author.username,post.content,post.timestamp.strftime("%H:%M:%S • %m/%d/%Y"),post.num_likes,False,post.pk])

    # Get page trying to be accessed
    page_num = int(request.GET.get('page') or 1)
    
    # Get current page of posts
    p = Paginator(data,10)
    posts = p.page(page_num)

    # Return list of posts as well as info on next/prev page status
    return JsonResponse({
        "posts": posts.object_list,
        "has_next": posts.has_next(),
        "has_prev": posts.has_previous(),
        "user": user
    }, safe=False)

@csrf_exempt
def edit(request, pk):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist"}, status=400)

        data = json.loads(request.body)
        if 'newContent' in data:
            post.content = data['newContent']
        if 'numLikes' in data:
            post.num_likes = data['numLikes']
            # If user liked post, create new Like object
            if data['liked']:
                like = Like(user=request.user, post=post)
                like.save()
            # Else, user unliked post, so remove existing Like object
            else:
                like = Like.objects.filter(user=request.user, post=post).get()
                like.delete()
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "Request must be PUT"}, status=400)
