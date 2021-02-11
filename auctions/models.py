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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    title = models.CharField(max_length=255, unique=True)
    description = RichTextField(max_length=255)
    starting_price = models.DecimalField(max_digits=19, decimal_places=2)
    category = models.CharField(max_length=2, choices=Category.choices,
                                default=Category.OTHERS,
                                blank=True)
    watchlist = models.ManyToManyField(to=User, related_name="watch", blank=True)
    current_bid = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        datetime = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        return f"{self.title} / current bid: ${self.current_bid} / posted: {datetime}"

class Bid(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bid = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        datetime = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        return f"{self.listing.title} / {self.user}'s bid: ${float(self.bid)} / posted: {datetime}"

class Photo(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_photos')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_photos")
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        datetime = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        return f"{self.listing.title} / {self.user} added URL: {self.image} / posted: {datetime}"
    
class Comment(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = RichTextField(blank=True)

    def __str__(self):
        datetime = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        return f"{self.listing.title} / {self.user}'s post / posted: {datetime}"
    
class Notification(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    ### Is who should be informed about closing ###
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_notifications")

    def __str__(self):
        datetime = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        return f"{self.user} / {self.listing.title} listing was closed / posted: {datetime}"
