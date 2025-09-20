
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("view_post", views.view_post, name = "view_post"),
    path("register", views.register, name="register"),
    path('like/<int:post_id>/', views.like, name='like'),
    path('profile/<str:user_name>',views.profile,name="profile"),
    path('toggle_follow/<str:user_name>/', views.toggle_follow, name='toggle_follow'),
]
