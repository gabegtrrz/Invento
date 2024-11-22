from django.db import models
from django.urls import reverse

# Validation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

# User Authentication Feature Imports
from django.contrib.auth.models import AbstractUser


# User Authentication Feature Models

class User(AbstractUser):
    business_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username



# CRUD Inventory Feature Models
# Reference SRS -- 7. Data Requirements


class Item_Model(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    minimum_inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Descriptive Attributes
    unit_measure = models.CharField(max_length=20)
    weight_grams = models.DecimalField(
        max_digits = 10,
        decimal_places = 5,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True
    )
    length_cm = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True
    )
    width_cm = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True
    )
    height_cm= models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True
    )

    def get_available_quantity(self):
        return sum(lot.available_quantity for lot in self.lots.all())
    
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
class Lot(models.Model):
    item = models.ForeignKey(Item_Model, on_delete=models.CASCADE, related_name='lots')
    lot_number = models.CharField(max_length=50, unique=True)
    received_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    initial_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def available_quantity(self):
        used_quantity = sum(movement.quantity for movement in self.movements.filter(movement_type='OUT'))
        return max(self.initial_quantity - used_quantity, 0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'lot_number'], name = 'unique_item_lot')
        ]
        # unique_together = ['item', 'lot_number']
        # deprecated ^
    
    def __str__(self):
        return f"{self.item.name} - Lot {self.lot_number}"


class Movement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        
        # 1st Element: The actual value stored in the database. 
        # 2nd ('Stock In'): The human-readable name displayed in forms or admin interfaces.
    ]
    


    movement_id = models.BigAutoField(primary_key=True)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    date = models.DateField(auto_now_add=True)
    performed_by = models.CharField(max_length=50)
    # supplier = models.CharField(max_length=50)
    purchase_price = models.DecimalField(_("Purchase Price"), 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    sale_price = models.DecimalField(
        _("Sale Price"), 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    notes = models.TextField(blank=True)
    
    def clean(self):
        # evaluates if quantity user wants to move now does not exceed what's left by
        # evaluating (total of quantity move out in the past + quantity needed now) 
        # greater than what was quantity when first deposited.
        if self.movement_type == 'OUT':
            past_lot_movements = Movement.object.filter(lot = self.lot, movement_type = 'OUT')
            total_num_past_out = sum(movement.quantity for movement in past_lot_movements)
            if total_num_past_out + self.quantity > self.lot.initial_quantity:
                raise ValidationError(f"Insufficient quantity in lot {self.lot.lot_number}")

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.lot} - {self.quantity}"