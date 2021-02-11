from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from .models import User, Bid, Comment, Listing, Photo, Notification
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Max, Count

# class max_count():
#     def __init__(self, obj, *args, **kwargs):
#         self.obj = obj

#     def get_max_bid(self):
#         return float(self.obj.bids.aggregate(Max('bid'))['bid__max'])

#     def get_count_bid(self):
#         return self.obj.bids.aggregate(Count("bid"))['bid__count']-1

class InfoForm(forms.ModelForm):
    
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_price', 'category']
        labels = {
            'title': 'Title',
            'starting_price': 'Enter the starting price',
            'category': 'Choose category (optional)',

        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category']
        labels = {
            'category': '',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CommForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': '',
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        labels = {
            'bid': '',
        }

        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ImageForm(forms.ModelForm): 
    ### This form is for Listing page ###
    class Meta:
        model = Photo
        fields = ['image']
        labels = {
            'image': '',
        }

        widgets = {
            'image': forms.FileInput(attrs={'class': 'custom-file-input',
                                            'id': 'inputGroupFile04',
                                            'aria-describedby': 'inputGroupFileAddon04',}),
        }

class ImageFormNew(forms.ModelForm): 
    ### This form is for newly created page ###
    class Meta:
        model = Photo
        fields = ['image']
        labels = {
            'image': '',
        }

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control',
                                            'id': 'inputGroupFile01',}),
        }

def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def new_listing(request):
    if request.method == 'POST':
        
        inf_form = InfoForm(request.POST)
        img_form = ImageFormNew(request.POST, request.FILES)

        if inf_form.is_valid() and img_form.is_valid():

            user = request.user
            title = inf_form.cleaned_data['title']
            description = inf_form.cleaned_data['description']
            starting_price = inf_form.cleaned_data['starting_price']
            category = inf_form.cleaned_data['category']
            if not category:
                inf_form.category = "OT"

            Listing(user=user, title=title,
                    description=description,
                    starting_price=starting_price).save()

            listing = Listing.objects.filter(title=title).get()
            image = img_form.cleaned_data['image']
            if image:
                Photo(user=user, listing=listing, image=image).save()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "img_form": ImageFormNew(),
                "comment_form": CommForm(),
                "bid_form": BidForm(),
                "category_form": CategoryForm(),
                "its_my": True,
                "request_user": request.user,
                })
        else:
            return render(request, "auctions/new_listing.html", {
                "inf_form": InfoForm(),
                "img_form": ImageFormNew(),
                })
    else:
        return render(request, "auctions/new_listing.html", {
            "inf_form": InfoForm(),
            "img_form": ImageFormNew(),
            })


@login_required
def listing(request, title):
    pass
#     listing = Listing.objects.filter(title=title).first()
#     user = User.objects.filter(username=request.user).first()
#     bid_error = None
#     if listing:
#         listing_obj = max_count(listing)
#         its_my = listing.user == request.user

#         if request.method == 'POST':
#             bidform = BidForm()
#             if request.FILES.get('image'):
#                 imgform = ImageForm(request.FILES)
#                 if imgform.is_valid():
#                     image = imgform.cleaned_data["image"]
                    
#                     Photo(listing=listing, image=image).save()
#                 #else:
#                     #return render(request, 'auctions/error.html', {
#                         #"message": "Image isn\'t valid"
#                     #})
#             if request.POST.get('comment'):
#                 commentform = CommForm(request.POST)
#                 if commentform.is_valid():
#                     comment = commentform.cleaned_data["comment"]
#                     Comment(listing=listing,
#                                 username=request.user, comment=comment).save()
#                 #else:
#                     #return render(request, 'auctions/error.html', {
#                         #"message": "comment isn\'t valid"
#                     #})
#             if request.POST.get('bid'):
#                 bidform = BidForm(request.POST)
#                 if bidform.is_valid():
#                     bid = bidform.cleaned_data["bid"]
#                     if float(bid) <= listing_obj.get_max_bid():
#                         bid_error = 'Your bid should be higher than the current price!'
#                         bidform = BidForm(request.POST)
#                     else:
#                         Bid(listing=listing, username=request.user, bid=bid).save()
#                         listing.current_price = listing_obj.get_max_bid()
#                         listing.save()
#                         bidform = BidForm()
#                         #else:
#                             #return render(request, "auctions/error.html", {
#                                 #"message": 'Please change the bid, this bid already exists',
#                             #})
#                     #else:
#                         #return render(request, "auctions/error.html", {
#                             #"message": 'bid isn\'t valid',
#                         #})
#             if request.POST.get("category"):
#                 catform = CategoryForm(request.POST)
#                 if catform.is_valid():
#                     category = catform.cleaned_data["category"]
#                     listing.category = category
#                     listing.save()
#                 #else:
#                     #return render(request, "auctions/error.html", {
#                         #"message": 'category isn\'t valid',
#                 #})       
#             if request.POST.get('add') or request.POST.get('remove'):
#                 if request.POST.get("add") == 'yes':
#                     listing.watchlist.add(user)
#                 if request.POST.get('remove') == 'yes':
#                     listing.watchlist.remove(user)

#             if request.POST.get('close'):
#                 listing.is_active=False
#                 listing.save()
#                 b = Bid.objects.all().filter(listing=listing)
#                 u = User.objects.all()

#                 for i in u:
#                     if b.filter(username=i.username):
#                         Notification(user=i, notification=listing.title).save()

#             winner = Bid.objects.filter(bid=listing_obj.get_max_bid()).first().username
#             return render(request, "auctions/listing.html", {
#                 "listing": listing,
#                 "img_form": ImageForm(),
#                 "comment_form": CommForm(),
#                 "bid_form": bidform,
#                 "bid_count": listing_obj.get_count_bid(),
#                 "winner": winner,
#                 "category_form": CategoryForm(),
#                 "its_my": its_my,
#                 "owner": str(winner)==str(request.user),
#                 "bid_error": bid_error,
#             })
#         else:
#             winner = Bid.objects.filter(bid=listing_obj.get_max_bid()).first().username
#             return render(request, "auctions/listing.html", {
#                 "listing": listing,
#                 "img_form": ImageForm(),
#                 "comment_form": CommForm(),
#                 "bid_form": BidForm(),
#                 "bid_count": listing_obj.get_count_bid(),
#                 "winner": winner,
#                 "category_form": CategoryForm(),
#                 "its_my": its_my,
#                 "owner": str(winner)==str(request.user),
#                 "bid_error": None,
#             })
#     else:
#         return render(request, "auctions/error.html", {
#             "message": 'Listing doesn\'t exists',
#         })

@login_required
def my_listings(request):

    my_listings = User.objects.filter(username=request.user).get().user_listings.all()

    return render(request, "auctions/my_listings.html", {
        "listings": my_listings,
    })

@login_required
def category(request, category):
    
    if category=='HM':
        category_display = "Home"
    if category=='EL':
        category_display = "Electronics"
    if category=='FS':
        category_display = "Fashion"
    if category=='HB':
        category_display = "Health & Beauty"
    if category=='GR':
        category_display = "Motors"
    if category=='CL':
        category_display = "Collectibles"
    if category=='SP':
        category_display = "Sports"
    if category=='GA':
        category_display = "Garden"        
    if category=='DE':
        category_display = "Deals"
    if category=='UT':
        category_display = "Under $10"
    if category=='PT':
        category_display = "Pets"
    if category=='TY':
        category_display = "Toys"
    if category=='OT':
        category_display = "Others"

    cat_listings = Listing.objects.filter(category=category)
    if cat_listings:
        category_display = cat_listings.first().get_category_display()

    return render(request, "auctions/category.html", {
        "listings": cat_listings,
        "category_display": category_display,
    })

@login_required
def watchlist(request):

    if request.method == "GET":
        
        u = User.objects.filter(username=request.user).get()
        watchlist = u.watch.all()

        return render(request, "auctions/watchlist.html", {
            "listings": watchlist,
        })
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def error(request):

    return HttpResponseRedirect(reverse("error"))

@login_required
def notifications(request):

    if request.method == "POST":
        title = request.POST['notification']
        L = Listing.objects.filter(title=title).get()
        Notification.objects.filter(user=request.user).filter(listing=L).get().delete()
        notifications = Notification.objects.filter(user=request.user).all()
        return render(request, 'auctions/notifications.html', {
            "notifications": notifications,
        })
        

    elif request.method == "GET":
        notifications = Notification.objects.filter(user=request.user).all()
        return render(request, 'auctions/notifications.html', {
            "notifications": notifications,
        })

