from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import User, Post, comment, Follow


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

def profile(request, user_name):
    user_post = []
    user_profile = User.objects.get(username = user_name)
    posts = Post.objects.filter(username = user_name).order_by('-timestamp')
    for post in posts:
        user_post.append(post)
    return render (request, "network/profile.html",{
        "username":user_name,
        "user_posts":user_post,
        "userid" : user_profile.id
    })
def like(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.likes.filter(id = request.user.id):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect ('index')
@csrf_exempt
def follow(request,user_id):
    user_to_follow = get_object_or_404(Follow, id = user_id)
    if request.method == "POST":
        follow_object, created = Follow.objects.get_or_create(
            follower = request.user,
            following = user_to_follow
        )
        if not created:
            follow_object.delete()
    return JsonResponse({
        "message_follow": "success",
        "followers": user_to_follow.number_of_followers,
        "follwing": user_to_follow.number_of_following
    })



