from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.category_name}"

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    
class Auction_list(models.Model):
    item_name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price_bid")
    image_url = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    
    def __str__(self):
        return f"{self.item_name}"
    
class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Auction_list, on_delete=models.CASCADE, blank=True, null=True, related_name="auction_list_comment")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.commentator} commented {self.listing}"
    

