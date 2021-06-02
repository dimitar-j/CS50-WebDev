from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [
        ('FSHN','Fashion'),
        ('TOYS', 'Toys'),
        ('ELEC', 'Electronics'),
        ('HOME', 'Home')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="listings",null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500,blank=True)
    category = models.CharField(max_length=4,blank=True,choices=CATEGORIES)
    start_price = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    current_price = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Listing {self.id}: {self.title}"


class Bid(models.Model):
    bid = models.DecimalField(max_digits=64, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bids", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="bids", null=True)

    def __str__(self) -> str:
        return f"{self.bidder} bid ${self.bid} on {self.listing}"

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    author = models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE, null=True)

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="saved_by")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="saved_items")

    def __str__(self):
        return f"{self.item} saved by {self.user}"
