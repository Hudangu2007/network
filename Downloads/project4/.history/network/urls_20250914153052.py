
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post_listing", views.post_listing, name = "post_listing"),
    path("register", views.register, name="register")
]
