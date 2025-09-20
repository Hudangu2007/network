from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import User, Post, comment


def index(request):
    post_listings = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html",{
        "post_listings" : post_listings
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

def view_post(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        content = request.POST.get('content').strip()
        if content:
            new_post = Post(
                username = username,
                content = content
            )
            new_post.save()
            return redirect('index')
    return redirect('index')

@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes, 'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def profile(request, user_name):
    user_post = []
    user_profile = User.objects.get(username = user_name)
    posts = Post.objects.filter(username = user_name).order_by('-timestamp')
    for post in posts:
        user_post.append(post)
    user_post.append(post)
    return render (request, "network/profile.html",{
        "username":user_name,
        "followers": user_profile.follower,
        "following":user_profile.following,
        "user_posts":user_post
    })

def toggle_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id = post_id)
        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            post.likes -= 1
            liked = False
        else:
            post.liked_by.add(user)
            post.likes +=1
            liked = True
        post.save()
        return JsonResponse({'likes': post.likes,, 'liked': liked})


