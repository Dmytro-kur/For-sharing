from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import re
from ckeditor.fields import RichTextField

class User(AbstractUser):
    pass

class Listing(models.Model):

    class Category(models.TextChoices):
        HOME = 'HM', _('Home')
        ELECTRONICS = 'EL', _('Electronics')
        FASHION = 'FS', _('Fashion')
        HEALTH_BEAUTY = 'HB', _('Health & Beauty')
        MOTORS = 'GR', _('Motors')
        COLLECTIBLES = 'CL', _('Collectibles')
        SPORTS = 'SP', _('Sports')
        HOME_GARDEN = 'GA', _('Garden')
        DEALS = 'DE', _('Deals')
        UNDER_TEN = 'UT', _('Under $10')
        PETS = 'PT', _('Pets')
        TOYS = 'TY', _('Toys')
        OTHERS = 'OT', _('Others')
        __empty__ = _('(Unknown)')

    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255, unique=True)
    description = RichTextField()
    starting_bid = models.DecimalField(max_digits=19, decimal_places=2)
    category = models.CharField(max_length=2, choices=Category.choices,
                                default=Category.OTHERS,
                                blank=True)
    watchlist = models.ManyToManyField(to=User, related_name="watch", blank=True)
    current_price = models.DecimalField(max_digits=19, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"/{self.title}/ starting bid: ${self.starting_bid} / posted: {self.datetime}"

class Photo(models.Model):
    listing = models.ForeignKey(Listing, default=None,
                             on_delete=models.CASCADE,
                             related_name='listing_photos')
    
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        return f"{self.listing.title}"
    
class Comment(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    username = models.CharField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "comments")
    comment = RichTextField(blank=True)

    def __str__(self):
        return f"{self.username} said about {self.listing.title}: \"{self.comment}\", Created {self.datetime}"
    
class Bid(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    username = models.CharField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=19,
                             decimal_places=2,
                              blank=True)

    def __str__(self):
        return f"{self.username} makes a bid on {self.listing.title} listing: ${float(self.bid):.2f}"

class Notification(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}, {self.notification}"
