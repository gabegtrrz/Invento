from django import forms

# User Authentication Feature Imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# make sure to have configured your settings.py AUTH_USER_MODEL 
# Format: 'app_name.Model_name'

from . models import Item_Model




# User Authentication Feature Forms -----


# instantiate user model
User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    






# CRUD Inventory Feature Forms -----
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item_Model
        fields = '__all__'
        # labels -> dictionary of different key-value pair sets
        labels = {
            'item_id': 'Item ID',
            'name': 'Name',
            'sku': 'SKU',
            'price': 'Price',
            'quantity': 'Quantity',
            'supplier': 'Supplier',
        }
        widgets = {
            'item_id': forms.NumberInput(attrs={'placeholder':'e.g 1', 'class':'form-control'}),
            'name': forms.TextInput(attrs={'placeholder':'Item Name', 'class':'form-control'}),
            'sku': forms.TextInput(attrs={'placeholder':'e.g. ABC_001', 'class':'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder':'Price', 'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder':'e.g. 1', 'class':'form-control'}),
            'supplier': forms.TextInput(attrs={'placeholder':'e.g. Acme Inc.', 'class':'form-control'}),
        }
