from django.shortcuts import render, redirect

# App Classes
from . models import Item_Model
from . forms import ItemForm


# Create your views here.

# Home View
def index_view(request):
    return render(request, 'InventoApp/index.html')


# Create View
def create_view(request):
    form = ItemForm()




# Read View
# Update View
# Delete View