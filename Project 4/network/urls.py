
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>/", views.user, name="user"),
    path("following",views.following,name="following"),
    path("posts",views.posts,name="posts"),
    path("edit/<int:pk>",views.edit,name="edit")
]
