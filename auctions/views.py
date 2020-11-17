from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User, AuctionListing, CategoryChoices, Bid, Comment
from .forms import NewListingForm, NewBidForm, NewCommentForm, NewCategoryForm


def index(request):
    # listing = AuctionListing.objects.all()
    # myaggregate = AuctionListing.objects.filter(pk=1).aggregate(
    # mymax=Max('item__currentBid'))  # for test
    listing = AuctionListing.objects.annotate(maxBid=Max('item__currentBid'))
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

    message = None
    status = statusManager(request, item_id)
    item = status["item"]
    bids = status["bids"]

    user = watchlistManager(request, item)  # watchlist
    # all userwatchlist related to this item tested
    watchlistStatus = item.userWatchlist.all()
    commentList = commentManager(item)
    if request.method == "POST":

        if "comment" in request.POST:
            bidForm = NewBidForm()
            commentForm = NewCommentForm(request.POST)
            if commentForm.is_valid():
                userComment = commentForm.cleaned_data["comments"]
                comment = Comment.objects.create(
                    user=user, itemComment=item, comment=userComment)
            else:
                return render(request, "auctions/listing.html", {
                    "item": item,
                    "isInWatchlist": watchlistStatus.filter(id=user.id).exists(),
                    "message": message,
                    "bidForm": bidForm,
                    "commentForm": commentForm,
                    "nbids": status["nbids"],
                    "currentBid": status["currentBid"],
                    "commentList": commentList
                })
        else:
            bidForm = NewBidForm(request.POST)
            commentForm = NewCommentForm()
            if bidForm.is_valid():
                userBid = bidForm.cleaned_data["bid"]
                message = bidsManager(bids, userBid, user, item)  # bids
            else:
                return render(request, "auctions/listing.html", {
                    "item": item,
                    "isInWatchlist": watchlistStatus.filter(id=user.id).exists(),
                    "message": message,
                    "bidForm": bidForm,
                    "commentForm": commentForm,
                    "nbids": status["nbids"],
                    "currentBid": status["currentBid"],
                    "commentList": commentList
                })

    bidForm = NewBidForm()
    commentForm = NewCommentForm()
    newStatus = statusManager(request, item_id)
    newCommentList = commentManager(item)
    nbids = newStatus["nbids"]
    currentBid = newStatus["currentBid"]
    return render(request, "auctions/listing.html", {
        "item": item,
        "isInWatchlist": watchlistStatus.filter(id=user.id).exists(),
        "message": message,
        "bidForm": bidForm,
        "commentForm": commentForm,
        "nbids": nbids,
        "currentBid": currentBid,
        "commentList": newCommentList
    })


@login_required(login_url="index")
def watchlist(request):
    currentUser = User.objects.get(id=request.user.id)
    watchlist = currentUser.watchlist.all()
    listing = watchlist.annotate(maxBid=Max('item__currentBid'))
    return render(request, "auctions/watchlist.html", {
        "watchlist": listing
    })


def categories(request):
    listing = AuctionListing.objects.annotate(maxBid=Max('item__currentBid'))
    if request.method == "POST":
        categoryForm = NewCategoryForm(request.POST)
        if categoryForm.is_valid():
            category = categoryForm.cleaned_data["category"]
            listed=AuctionListing.objects.filter(category=category).annotate(maxBid=Max('item__currentBid'))
        return render(request, "auctions/categories.html", {
            "listing": listed,
            "categoryForm": categoryForm
        })
    return render(request, "auctions/categories.html", {
        "listing": listing,
        "categoryForm": NewCategoryForm()
    })

# -----------------------------------------own functions---------------------------------------


def bidsManager(bids, userBid, user, item):
    message = None
    if not item.closed:
        if bids.exists():
            # get max value in Bid Table in currentBid field
            maxbid = bids.aggregate(Max('currentBid'))['currentBid__max']
            if(userBid > maxbid):
                if(bids.filter(currentUser_id=user.id).exists()):
                    newBid = bids.get(currentUser_id=user.id)
                    newBid.currentBid = userBid
                    newBid.save()
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
                message = f"  The bid must be at least as large as the starting price ${item.initialPrice}"
    return message


def watchlistManager(request, item):
    # user = request.user.username #for username
    user = request.user
    if "watchlistActive" in request.GET:
        if bool(request.GET["watchlistActive"]):
            user.watchlist.add(item)
        else:
            # remove condition
            user.watchlist.remove(item)
    return user


def statusManager(request, item_id):
    listItem = AuctionListing.objects.get(pk=item_id)
    bids = Bid.objects.filter(item=listItem)
    # usersInBid=listItem.item.values_list('currentUser', flat=True) #it give me all user who have made bids in the item from Auctionlisting table and i can access directly to a field in bids table
    nbids = bids.count()
    if bids.exists():
        maxbid = bids.aggregate(Max('currentBid'))['currentBid__max']
        maxBidPerUser = listItem.item.values('currentUser').annotate(
            Max('currentBid'))  # it give me max bid made per user in this item
        currentBid = maxBidPerUser.get(
            currentBid__max=maxbid)  # as a dict not query

        if "close" in request.GET:
            winnerBid = bids.get(currentBid=maxbid)
            winner = winnerBid.currentUser
            listItem.closed = True
            listItem.winner = winner
            listItem.save()
    else:
        currentBid = None
    return {"item": listItem, "bids": bids, "nbids": nbids, "currentBid": currentBid}


def commentManager(item):
    commentList = None
    commentList = Comment.objects.filter(itemComment=item)
    return commentList
