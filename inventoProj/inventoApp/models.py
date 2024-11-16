from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# User Authentication Feature Imports
from django.contrib.auth.models import AbstractUser


# User Authentication Feature Models

class User(AbstractUser):
    business_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


# CRUD Inventory Feature Models

class Item_Model(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(primary_key=True, max_length=50, unique=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    minimum_inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Descriptive Attributes
    unit_measure = models.CharField(max_length=50)
    weight_grams = models.DecimalField(
        max_digits = 10,
        decimal_places = 5,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    length_cm = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    width_cm = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    height_cm= models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def current_inventory(self):
        return sum(inventory.quantity for inventory in self.inventoryitem_set.all())

    def __str__(self):
        return f"{self.name} ({self.sku})"
    

    def __str__(self):
        return f"{self.name} | ID: {self.item_id} | SKU: {self.sku}"
