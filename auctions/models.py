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
    country = models.CharField(max_length=64, blank=True)

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
    price = models.DecimalField(max_digits=11, decimal_places=2)
    dateCreated = models.DateTimeField(auto_now=True)
    image = models.URLField(blank=True)
    sold = models.BooleanField(default=False)
    category = models.CharField(
        max_length=2, choices=CategoryChoices.choices, default=CategoryChoices.UNCATEGORY, blank=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    item = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="item")
    actualBid = models.DecimalField(max_digits=11, decimal_places=2)
    actualUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userBid")
    users = models.ManyToManyField(User, related_name="Bids")

    def __str__(self):
        return f"{self.item} {self.actualBid} {self.actualUser}"


class Coment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userComent")
    user
    itemComent = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="itemComent")
    coment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.itemComent} {self.user} {self.coment}"
