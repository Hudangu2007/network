from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import User, Post, comment, Follow

def taking_post(request):
    post_listings = Post.objects.all().order_by('-timestamp')
    #return JsonResponse({'post_listings': post_listings}) làm như này là sai vì class Post trả về Query Set
    #Còn nếu muốn return Json data ta cần biến nó thành 1 dictionary đã ==> Fix như sau:
    posts_data =[]
    for post in post_listings:
        posts_data.append({
            'id':post.id,
            'username': post.username,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'content': post.content,    
            'number_of_likes': post.number_of_likes(),
        })
    return JsonResponse({'post_listings': posts_data})

def index(request):
    return render(request, "network/index.html")

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

def like(request, post_id, mailbox):
    post = get_object_or_404(Post, id = post_id)
    if post.likes.filter(id = request.user.id):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    if mailbox == 'following_post':
        return redirect('following_post', username=request.user.username) #cần thêm username để chuyển về đúng trang following của user hiện tại
    if mailbox == 'profile':
        return redirect('profile', username=request.user.username) #cần thêm username để chuyển về đúng trang profile của user hiện tại
    return redirect (mailbox)

@login_required
def toggle_follow(request, username):
    if request.method == "POST":
        try:
            # Lấy user cần follow/unfollow
            target_user = get_object_or_404(User, username=username)
            current_user = request.user
            
            # Kiểm tra xem đã follow chưa
            follow_relationship = Follow.objects.filter( #Tìm xem trong class Follow có người nào như này ko
                follower=current_user,
                following=target_user
            ).first()
            
            if follow_relationship: 
                # Đã follow -> Unfollow
                follow_relationship.delete()
                is_following = False
                action = 'unfollowed'
            else:
                # Chưa follow -> Follow
                Follow.objects.create(
                    follower=current_user,
                    following=target_user
                )
                is_following = True
                action = 'followed'
            
            # Đếm số followers hiện tại của target_user
            #followers_count = target_user.followers.count() #followers này là related_name trong class Follow
            #following_count = target_user.following.count()
            #Django sẽ tự động tạo ra:
            #user.followers - Trả về tất cả Follow objects mà user này là following (tức những người follow user này)
            #user.following - Trả về tất cả Follow objects mà user này là follower (tức những người mà user này đang follow)
            
            return redirect('profile', username=username)
                      
        except User.DoesNotExist:
            return redirect ('profile')

def taking_profile(request, username):
    user_profile = get_object_or_404(User, username = username)
    followers_count = user_profile.followers.count() #Trả về query set các Follow objects mà có following = user_profile
    following_count = user_profile.following.count()
    posts = Post.objects.filter(username = username).order_by('-timestamp')
    riel_posts = []
    for post in posts:
        riel_posts.append({
            'id':post.id,
            'username': post.username,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'content': post.content,    
            'number_of_likes': post.number_of_likes(),
        })
    return JsonResponse({
        "userid":user_profile.id,
        'followers_count': followers_count,
        'following_count': following_count,
        #'posts': list(posts.values()),  # Convert QuerySet to list of dicts
        'posts': riel_posts
    })
def profile(request, username):
    user_post = []
    user_profile = User.objects.get(username = username)
    followers_count = user_profile.followers.count() #Trả về query set các Follow objects mà có following = user_profile
    following_count = user_profile.following.count()
    posts = Post.objects.filter(username = username).order_by('-timestamp')
    for post in posts:
        user_post.append(post)
    is_following = False #Phải có dòng này để phòng trường hợp khi user chưa đăng nhập thì is_following sẽ = undefined dẫn đến lỗi trong html
    if request.user.is_authenticated and request.user != user_profile:
        is_following = Follow.objects.filter(
        follower=request.user,
        following=user_profile
        ).exists()
    return render (request, "network/profile.html",{
        "username":username,
        "user_posts":user_post,
        "userid":user_profile.id,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

def taking_follow(request, username):
    recent_user = get_object_or_404(User, username = username) #lấy ra user hiện tại đang log in
    user_followings = recent_user.following.all() # lấy những người mà user hiện tại đang follow
    following_usernames = recent_user.following.values_list('following__username', flat=True) #tạo 1 list các userame
    #recent_user.following vẫn là truy cập đến related name 
    #values_list là tạo ra 1 list chỉ lấy các giá trị cụ thể của user
    #following__username = lấy username của các objects
    #flat = True để tạo định dạng ['alice', 'bob', 'charlie']
    view_posts = Post.objects.filter(username__in = following_usernames).order_by('-timestamp')
    posts_data =[]
    for post in view_posts:
        posts_data.append({
            'id':post.id,
            'username': post.username,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'content': post.content,    
            'number_of_likes': post.number_of_likes(),
        })
    return JsonResponse({'follow_listings': posts_data})
def following_post(request, username):
    recent_user = get_object_or_404(User, username = username) #lấy ra user hiện tại đang log in
    user_followings = recent_user.following.all() # lấy những người mà user hiện tại đang follow
    following_usernames = recent_user.following.values_list('following__username', flat=True) #tạo 1 list các userame
    #recent_user.following vẫn là truy cập đến related name 
    #values_list là tạo ra 1 list chỉ lấy các giá trị cụ thể của user
    #following__username = lấy username của các objects
    #flat = True để tạo định dạng ['alice', 'bob', 'charlie']
    view_posts = Post.objects.filter(username__in = following_usernames).order_by('-timestamp')
    #field__in=[list_of_values] → SQL: WHERE field IN (value1, value2, ...)
    #field=value → SQL: WHERE field = value
    #field__contains=value → SQL: WHERE field LIKE '%value%'
    total_post = view_posts.count()
    pagination_count = int(total_post/10)
    if(total_post%10 != 0):
        pagination_count +=1
    soluong = range(1, pagination_count+1) #tạo 1 array số thì mới tương tác được với trong html
    return render(request, 'network/followingpost.html',{
        'soluong': soluong,
        'pagination_count': pagination_count,
    })

def savepost(request, id):
    currentpost = Post.objects.get(id = id)
    currentpost.content = newcontent
    currentpost.save()
    return redirect ('profile')





        