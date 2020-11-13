from django.contrib import admin

from .models import User, AuctionListing, Bid, Comment

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display=("title","description","initialPrice","dateCreated","closed","category","owner","winner")

class BidAdmin(admin.ModelAdmin):
    list_display=("currentUser","currentBid","item")

class CommentAdmin(admin.ModelAdmin):
    list_display=("date","user","itemComment","comment")

class UserAdmin (admin.ModelAdmin):
    filter_horizontal=("watchlist",)

admin.site.register(User,UserAdmin)
admin.site.register(AuctionListing,AuctionAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Comment,CommentAdmin)
