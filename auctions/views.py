from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Auction_list, Comment, Bid

def listing(request, listing_id):
    listing_data = Auction_list.objects.get(pk=listing_id)
    inWatchlist = request.user in listing_data.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html",{"lists":listing_data, "inWatchlist":inWatchlist, "all_comments":all_comments, "is_owner":is_owner})

def close_auction(request, listing_id):
    listing_data = Auction_list.objects.get(pk=listing_id)
    listing_data.is_active = False
    listing_data.save()
    inWatchlist = request.user in listing_data.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html",{"lists":listing_data, "inWatchlist":inWatchlist, "all_comments":all_comments, "is_owner":is_owner, "update": True, "message":"Auction is closed"})

def add_bid(request, listing_id):
    new_bid = request.POST['add_bid']
    listing_data = Auction_list.objects.get(pk=listing_id)
    inWatchlist = request.user in listing_data.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    if int(new_bid) > listing_data.price.bid:
        update_bid = Bid(user=request.user, bid=int(new_bid))
        update_bid.save()
        listing_data.price = update_bid
        listing_data.save()
        return render(request, "auctions/listing.html", {"lists":listing_data, "is_owner":is_owner, "message": "ok.", "inWatchlist":inWatchlist, "all_comments":all_comments, "update": True})
    else:
        return render(request, "auctions/listing.html", {"lists":listing_data, "is_owner":is_owner, "message": "fail.", "inWatchlist":inWatchlist, "all_comments":all_comments, "update": False})

def add_comment(request, listing_id):
    listing_data = Auction_list.objects.get(pk=listing_id)
    current_user = request.user
    message = request.POST['new_comment']
    new_comment = Comment(commentator=current_user, listing=listing_data, message=message)
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def deleteWatchlist(request, listing_id):
    listing_data = Auction_list.objects.get(pk=listing_id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def addWatchlist(request, listing_id):
    listing_data = Auction_list.objects.get(pk=listing_id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def userWatchlist(request):
    current_user = request.user
    userWatch = current_user.watchlist.all()
    return render(request,"auctions/watchlist.html", {"lists":userWatch})

def index(request):
    active_auctions = Auction_list.objects.filter(is_active=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {"lists":active_auctions, "categories":allCategories})

def category_selection(request):
    if request.method == "POST":
        select_category = request.POST['category']
        category = Category.objects.get(category_name=select_category)
        active_auctions = Auction_list.objects.filter(is_active=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {"lists":active_auctions, "categories":allCategories})
    
def create_auctions(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create_auctions.html", {"categories": allCategories})
    else:
        item_name = request.POST["item_name"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = request.POST["price"]
        category = request.POST["category"]

        current_user = request.user
        category_data = Category.objects.get(category_name=category)

        bid = Bid(bid=int(price), user=current_user)
        bid.save()

        new_auction = Auction_list(item_name=item_name, description=description, image_url=image_url, price=bid, category=category_data, owner=current_user)
        new_auction.save()

        return HttpResponseRedirect(reverse(index))

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
