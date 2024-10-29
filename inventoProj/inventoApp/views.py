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
# this is where we want to instantiate/create an item RECORD/Object,
# or facilitate its creation by providing the form to the user.

    form = ItemForm()

    # Logic when POST
    if request.method == 'POST':
        form = request.POST
        if form.is_valid():
            form.save()
            return redirect('item_list')
    
    # Logic to render the FORM for filling it up
    # Remember that Django Views handle the logic.
    else:
        return render(request, 'InventoApp/item_form.html', {'form':form})


# Read View
def item_list_view(request):
    items = Item_Model.objects.all()
    return render(request, 'item_list', {'items':items})


# Update View


# Delete View