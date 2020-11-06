from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, CategoryChoices, Bid
from .forms import NewListingForm


def index(request):
    listing = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listing": listing
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


@login_required(login_url="index")
def new(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            price = form.cleaned_data["price"]
            imageURL = form.cleaned_data["imageURL"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            owner = request.user
            # add var to table
            auction = AuctionListing(title=title, initialPrice=price, image=imageURL,
                                     category=category, description=description, owner=owner)
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            # form.fields['category'].choices = CategoryChoices.choices#add a choices in category
            return render(request, "auctions/new.html", {
                "form": form
            })
    form = NewListingForm()
    return render(request, "auctions/new.html", {
        "form": form
    })


@login_required(login_url="index")
def listing(request, item_id):
    item = AuctionListing.objects.get(pk=item_id)
    # user = request.user.username #for username
    user = request.user

    if request.method == "POST":
        userBid = float(request.POST["bid"])
        # initial=AuctionListing.objects.get(owner__id=user.id).initialPrice#initialprice for owner's listing with current owner
    
    #all userwatchlist related to this item
    
    if "watchlistActive" in request.GET:
        if bool(request.GET["watchlistActive"]):
            user.watchlist.add(item)
        else:
            #remove condition
            user.watchlist.remove(item)

    watchlistStatus=item.userWatchlist.all()
    return render(request, "auctions/listing.html", {
        "item": item,
        "isInWatchlist":watchlistStatus.filter(id=user.id).exists()
    })

    