from django.contrib import admin

from .models import User, AuctionListing, Bid, Coment

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display=("title","description","price","dateCreated","sold","category","owner")

class BidAdmin(admin.ModelAdmin):
    list_display=("item","actualBid","actualUser")

admin.site.register(User)
admin.site.register(AuctionListing,AuctionAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Coment)
