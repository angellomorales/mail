from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User, AuctionListing, CategoryChoices, Bid
from .forms import NewListingForm, NewBidForm


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
    message = None
    user = request.user
    bids = Bid.objects.filter(item=item)

    # ----------watchlist---------------------
    if "watchlistActive" in request.GET:
        if bool(request.GET["watchlistActive"]):
            user.watchlist.add(item)
        else:
            # remove condition
            user.watchlist.remove(item)

    # all userwatchlist related to this item tested
    watchlistStatus = item.userWatchlist.all()
    # --------Bids---------------
    if request.method == "POST":

        form = NewBidForm(request.POST)
        if form.is_valid():
            userBid = form.cleaned_data["bid"]

            if (bids.exists()):
                # get max value in Bid Table in currentBid field
                maxbid = bids.aggregate(Max('currentBid'))['currentBid__max']
                if(userBid > maxbid):
                    if(bids.filter(currentUser_id=user.id).exists()):
                        currentUser = bids.get(currentUser_id=user.id)
                        currentUser.currentBid = userBid
                        currentUser.save()
                    else:
                        newBid = Bid.objects.create(
                            currentUser=user, currentBid=userBid, item=item)
                else:
                    message = f"The bid must be greater than { maxbid }"
            else:
                if (userBid >= item.initialPrice):
                    newBid = Bid.objects.create(
                        currentUser=user, currentBid=userBid, item=item)
                else:
                    message = "  The bid must be at least as large as the starting price"
        else:
            return render(request, "auctions/listing.html", {
                "item": item,
                "isInWatchlist": watchlistStatus.filter(id=user.id).exists(),
                "message": message,
                "form": form
            })

    form = NewBidForm()
    return render(request, "auctions/listing.html", {
        "item": item,
        "isInWatchlist": watchlistStatus.filter(id=user.id).exists(),
        "message": message,
        "form": form
    })
