from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("category/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("error", views.error, name="error"),
    path("notifications", views.notifications, name="notifications"),
    path("<str:title>", views.listing, name="listing"),

]
