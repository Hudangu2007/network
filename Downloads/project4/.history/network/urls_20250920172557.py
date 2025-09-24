
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("view_post", views.view_post, name = "view_post"),
    path("register", views.register, name="register"),
    path('like/<int:post_id>/<str:mailbox>', views.like, name='like'),
    path('profile/<str:username>',views.profile,name="profile"),
    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('following_post/<str:username>', views.following_post, name = "following_post"),
    path('taking_post', views.taking_post, name = "taking_post"),
]
