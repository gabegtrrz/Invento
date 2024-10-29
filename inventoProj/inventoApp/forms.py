from django import forms
from . models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
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
            'quantity': forms.NumberInput(attrs={'placeholder':'e.g 1', 'class':'form-control'}),
            'supplier': forms.TextInput(attrs={'placeholder':'e.g Acme Inc.', 'class':'form-control'}),
        }
