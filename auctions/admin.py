from django.contrib import admin
from .models import User, Category, Auction_list, Comment, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_list)
admin.site.register(Comment)
admin.site.register(Bid)