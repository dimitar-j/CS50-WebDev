from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("closelisting/<int:listing_id>", views.close_listing, name="closelisting"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("categories",views.categories,name="categories"),
    path("<str:category_name>",views.category,name="category")
]
