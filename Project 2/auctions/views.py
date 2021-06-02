from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.aggregates import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import Listing, Watchlist, Bid, Comment
from .util import check_bid
from django.contrib.auth.decorators import login_required

from .models import User

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description', 'image', 'category', 'start_price']
        exclude = ('current_price','user','active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'start_price': forms.NumberInput(attrs={'class': 'form-control', "max_digits": 4, "decimal_places": 2, "default":0.00})
        }


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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

def new_listing(request):
    if request.method=="POST":

        form = NewListingForm(request.POST)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.current_price = request.POST.get('start_price')
            form.save()

        return HttpResponseRedirect(reverse("index"))
    else:    
        if request.user.is_authenticated:
            return render(request, "auctions/newlisting.html", {
                "form": NewListingForm()
            })
        else:
            return render(request, "auctions/login.html")

def listing(request, listing_id):

    highest_bidder = None
    error_msg = ""

    # Get the current item
    listing = Listing.objects.get(pk=listing_id)

    # Check if listing has bids and save highest bidder
    if listing.bids.all():
        bids = listing.bids.all()
        highest_bid = bids.order_by('-bid').first()
        highest_bidder = getattr(highest_bid,'bidder')

    # Check if request method is POST
    if request.method == "POST":

        # Check if user is saving/removing item from watchlist
        if request.POST.get('action') == "Add to Watchlist" or request.POST.get('action') == "Remove from Watchlist":

            # If item already saved by user, remove it
            if Watchlist.objects.filter(item=listing, user=request.user):
                Watchlist.objects.filter(item=listing, user=request.user).delete()
            
            # If item is not saved by user, add it to their watchlist
            else:
                watchlist = Watchlist(item=listing, user=request.user)
                watchlist.save()

        # Check if user is making a bid
        elif request.POST.get('action') == "Bid!":

            # Check if placed bid is empty
            if request.POST.get('bid')=="":
                error_msg = "Please enter a bid larger than or equal to the current price"

            # Check if listing has a bid
            elif not listing.bids.all():

                # Check if placed bid is higher than starting price
                if float(request.POST.get('bid')) < listing.start_price:
                    error_msg = "Please enter a bid larger than or equal to the current price"
                else:
                    bid = Bid(bid=request.POST.get('bid'),bidder=request.user,listing=listing)
                    bid.save()
                    listing.current_price = bid.bid
                    listing.save()

            # Check if placed bid is higher than current bid
            elif check_bid(listing,float(request.POST.get('bid'))):
                bid = Bid(bid=request.POST.get('bid'),bidder=request.user,listing=listing)
                bid.save()
                listing.current_price = bid.bid
                listing.save()

            # Bid is not greater than current highest bid
            else:
                error_msg = "Please enter a bid larger than or equal to the current price"
        
        # Check if user is posting a comment
        elif request.POST.get('action') == "Post":
            content = request.POST.get('comment')
            comment = Comment(comment = content, author = request.user, listing = listing)
            comment.save()

    # Render listing page
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "authenticated": request.user.is_authenticated,
        "saved": Watchlist.objects.filter(item=listing, user=request.user),
        "error": error_msg,
        "current_price": listing.bids.all().aggregate(Max('bid')).get('bid__max'),
        "highest_bidder": highest_bidder,
        "comments": Comment.objects.filter(listing = listing)
    })


@login_required
def close_listing(request,listing_id):

    # Get the current item
    listing_obj= Listing.objects.get(pk=listing_id)
    listing_obj.active = False
    listing_obj.save()
    return listing(request,listing_id)

@login_required
def watchlist(request):
    qs = Watchlist.objects.filter(user=request.user)
    listings = []
    for i in qs:
        listings.append(i.item)
    print(f"SAVED LISTINGS: {listings}")
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def categories(request):
    categories_obj = Listing.CATEGORIES
    options = []
    for i in categories_obj:
        options.append(i[1])
    return render(request,"auctions/categories.html", {
        "categories": options
    })

def category(request, category_name):
    value = ""
    for i in Listing.CATEGORIES:
        if i[1] == category_name:
            value = i[0]
    print(f"VALUE: {value}")
    listings = Listing.objects.filter(category=value)
    print(f"{category_name} listings: {listings}")
    return render(request,"auctions/category.html",{
        "listings": listings,
        "category": category_name
    })