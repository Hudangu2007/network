
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("view_post", views.view_post, name = "view_post"),
    path("register", views.register, name="register"),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('profile/<str:user_name>',views.profile,name="profile")
]
