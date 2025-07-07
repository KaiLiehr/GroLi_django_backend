import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# AT FIRST no connection between user and lists or list items(just via household)
# should store and brand be their own items? for picture purposes? Are users allowed to add brands and stores?
# User: currently just AbstractUser 
# ITEM: id, name, brand(FK), store(FK), measurement(enum?), image
# Brand: name, logo,
# Store: name, logo,
# LISTITEM: ITEM(FK), amount, status(ENUM), description, created_by, created_at (maybe add: last_modified?by whom?)
# PriceItemInfo: Item(FK), price_per_1_unit, date
# List: name, creator, created_at, members: manytomany List-User relationship through membership model with inviter, joined_at 
# TODO: Create a property expected prize for listitem based on the most recent PriceItemInfo OR OVERRIDE default blank total price
# TODO: Add location info to PriceItemInfo


# Create your models here.
class User(AbstractUser):
    display_name = models.CharField(max_length=35, blank=False)

    def __str__(self):
        return self.display_name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brand_logos/",  blank=True, null=True)                 
    
    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="store_logos/", blank=True, null=True)                 

    def __str__(self):
        return self.name


# This is the core of what an item is for purposes of saving/re-use. Amount, created_at, created_by, description etc. are only added to the listItem
class Item(models.Model):
    class MeasurementChoices(models.TextChoices):
        GRAM = 'GRAM'
        KILO = 'KILOGRAM'
        LITER = 'LITER'
        MILILITER = 'MILILITER'
        UNIT = 'UNIT'   # Meant to be the generic default

    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True,)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, blank=True, null=True,)
    measurement = models.CharField(max_length=20, choices=MeasurementChoices.choices, default=MeasurementChoices.UNIT)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'brand', 'store'],
                name='unique_item_per_store_brand'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.brand.name}, {self.store.name})"
    

# The List model wich contains a number of users as members represented via membership many to many relation
# and a number of items represented via the manytomany ListItem intermediary model
class List(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(User, through="Membership",through_fields=("joined_list", "member"), related_name="joined_lists")
    items = models.ManyToManyField(Item, through="ListItem", related_name="parent_lists")

    def __str__(self):
        return f"{self.name}"


# Membership relation representing the manytomany relatioship between lists and users(Creator of list(Admin) is not member)
class Membership(models.Model):
    joined_list = models.ForeignKey(List, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    inviter = models.ForeignKey(User, related_name="membership_inviter", blank=True, null=True, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"List: {self.joined_list.name} Member: {self.member.username}"


# ManyToMany intermediary relationship between List and Item, this is the actual list entry
class ListItem(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        SOLVED = 'Solved'
        CANCELLED = 'Cancelled'

    list = models.ForeignKey(List, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    # expected prize during PENDING via PriceItemInfo(TODO), User should be prompted(via frontend?) to input the total prize for the chosen amount, when changing status to solved
    price_total = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    description = models.TextField()

    def __str__(self):
        return f"List: {self.list} Item: {self.item}"


# This allows users to document the price of the item in the store to then allow historical/brand/store price differences
class PriceItemInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price_per_1_unit = models.DecimalField(max_digits=20, decimal_places=6)
    date = models.DateTimeField(auto_now_add=True)
    # TODO Add location info, at least the country, for more meaningful comparisons

    def __str__(self):
        return f"{self.item} PRICE: {self.price_per_1_unit}"