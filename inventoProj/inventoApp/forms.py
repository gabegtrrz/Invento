from django import forms

# User Authentication Feature Imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# make sure to have configured your settings.py AUTH_USER_MODEL
# Format: 'app_name.Model_name'

from .models import Item_Model, Lot, Movement


# User Authentication Feature Forms -----


# instantiate user model
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# ----- ----- ----- ----- -----


# CRUD Inventory Feature Forms -----


# Create/Update
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item_Model
        fields = "__all__"
        # labels -> dictionary of different key-value pair sets
        labels = {
            "name": "Name",
            "sku": "SKU",
            "price": "Price",
            "minimum_inventory": "Minimum Inventory",
            "unit_measure": "Unit Measure",
            "weight_grams": "Weight (grams)",
            "length_cm": "Length (cm)",
            "width_cm": "Width (cm)",
            "height_cm": "Height (cm)",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Item Name", "class": "form-control"}
            ),
            "sku": forms.TextInput(
                attrs={"placeholder": "e.g. ABC_001", "class": "form-control"}
            ),
            "price": forms.NumberInput(
                attrs={"placeholder": "Price", "class": "form-control"}
            ),
            "unit_measure": forms.Select(
                attrs={
                    "placeholder": "(e.g. units, kilograms, etc.)",
                    "class": "form-control",
                }
            ),
            "minimum_inventory": forms.NumberInput(
                attrs={"placeholder": "Minimum Inventory", "class": "form-control"}
            ),
            "weight_grams": forms.NumberInput(
                attrs={"placeholder": "(optional)", "class": "form-control"}
            ),
            "length_cm": forms.NumberInput(
                attrs={"placeholder": "(optional)", "class": "form-control"}
            ),
            "width_cm": forms.NumberInput(
                attrs={"placeholder": "(optional)", "class": "form-control"}
            ),
            "height_cm": forms.NumberInput(
                attrs={"placeholder": "(optional)", "class": "form-control"}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        optional_fields = ['weight_grams', 'length_cm', 'width_cm', 'height_cm'
        ]
        for field in optional_fields:
            self.fields[field].required = False
            # The self.fields dictionary contains all the fields of the form keyed by their names.
            # By accessing self.fields[field], wer get the field instance corresponding to the name in the list we made (optional_fields).


class LotForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Item_Model.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    initial_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0.01
    )

    unit_cost = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    expiry_date = forms.DateField(required=False)

    class Meta:
        model = Lot
        fields = [
            "item",
            "lot_number",
            "received_date",
            "expiry_date",
            "initial_quantity",
            "unit_cost",
        ]
        labels = {
            "item": "Item",
            "received_date": "Received Date",
            "expiry_date": "Expiry Date",
            "initial_quantity": "Initial Quantity",
            "unit_cost": "Unit Cost",
        }
        widgets = {
            "received_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "expiry_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "initial_quantity": forms.NumberInput(
                attrs={"placeholder": "Initial Quantity", "class": "form-control"}
            ),
            "unit_cost": forms.NumberInput(
                attrs={"placeholder": "Unit Cost", "class": "form-control"}
            ),
        }


class StockInForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset=Item_Model.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    quantity = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    unit_cost = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    received_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    expiry_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    notes = forms.CharField(widget=forms.Textarea, max_length=250, required=False)


class StockOutForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset=Item_Model.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    notes = forms.CharField(widget=forms.Textarea, max_length=250, required=False)
