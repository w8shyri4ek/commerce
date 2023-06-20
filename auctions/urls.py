from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auctions/", views.create_auctions, name="create_auctions"),
    path("category_selection/", views.category_selection, name="category_selection"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("deleteWatchlist/<int:listing_id>/", views.deleteWatchlist, name="deleteWatchlist"),
    path("addWatchlist/<int:listing_id>/", views.addWatchlist, name="addWatchlist"),
    path("userWatchlist/", views.userWatchlist, name="userWatchlist"),
    path("add_comment/<int:listing_id>/", views.add_comment, name="add_comment"),
    path("add_bid/<int:listing_id>/", views.add_bid, name="add_bid"),
    path("close_auction/<int:listing_id>/", views.close_auction, name="close_auction")
]
