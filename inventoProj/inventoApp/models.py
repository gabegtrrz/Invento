from django.db import models

# User Authentication Feature Imports
from django.contrib.auth.models import AbstractUser





# User Authentication Feature Models

class User(AbstractUser):
    business_name = models.CharField(max_length=100, blank=True)



# CRUD Inventory Feature Models

class Item_Model(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} | ID: {self.item_id} | SKU: {self.sku}"


