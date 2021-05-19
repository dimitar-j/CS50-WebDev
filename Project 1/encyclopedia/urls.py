from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("search", views.search, name ="search"),
    path("newpage", views.new_page, name="newpage"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random", views.random_page, name="randompage")
]
