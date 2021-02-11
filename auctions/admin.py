from django.contrib import admin

from .models import Listing, User, Photo, Bid, Comment, Notification
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("user_permissions",)
    list_display = ("id", "username", "last_login",
                    "first_name", "last_name", 
                    "email", "is_staff", "is_superuser",
                    "is_active", "date_joined")

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    class InlinePhotoAdmin(admin.StackedInline):
        model = Photo

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ["watchlist"]
    inlines = [PhotoAdmin.InlinePhotoAdmin]
    class Meta:
        model = Listing

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Notification)
