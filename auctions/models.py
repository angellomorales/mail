from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

import datetime


class User(AbstractUser):
    # cuando hago migration y esta pass debo poner el nombre de la app de lo contrario
    # salta y no crea la carperta migration o la crea mal
    # si hay un error borrar cache initial y el archivo .sqlite3 y volver a hacer migracion sin el nombre de
    # la app
    # pass
    #use 'class' in the poiner when class is below the pointer
    watchlist=  models.ManyToManyField('AuctionListing',blank=True, related_name="userWatchlist")

    # def __str__(self):
    #     return f"{self.username}"


class CategoryChoices(models.TextChoices):
    UNCATEGORY = "UN", _("Uncategory")
    TOYS = "TO", _("Toys")
    FASHION = "FA", _("Fashion")
    ELECTRONICS = "EL", _("Electronics")
    HOME = "HO", _("Home")




class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    initialPrice = models.DecimalField(max_digits=11, decimal_places=2)
    dateCreated = models.DateTimeField(auto_now=True)
    image = models.URLField(blank=True)
    closed = models.BooleanField(default=False)
    category = models.CharField(
        max_length=2, choices=CategoryChoices.choices, default=CategoryChoices.UNCATEGORY, blank=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")
    winner=models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")

    def __str__(self):
        if self.closed:
            status="closed"
        else:
            status="available"
        return f"{self.title} Status: {status}"

class Bid(models.Model):
    currentBid = models.DecimalField(max_digits=11, decimal_places=2)
    currentUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="currentUser")
    item=models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="item")

    def __str__(self):
        return f"{self.currentUser} {self.currentBid} {self.item}"


class Coment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userComent")
    user
    itemComent = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="itemComent")
    coment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.itemComent} {self.user} {self.coment}"
