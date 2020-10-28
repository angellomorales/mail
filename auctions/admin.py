from django.contrib import admin

from .models import User, CategoryItem, AuctionListing, Bid, Coment

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display=("title","description","price","dateCreated","sold","category")

class BidAdmin(admin.ModelAdmin):
    list_display=("item","actualBid","actualUser")

admin.site.register(User)
admin.site.register(CategoryItem)
admin.site.register(AuctionListing,AuctionAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Coment)
