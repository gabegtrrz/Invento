from django.shortcuts import render, redirect

# App Classes
from . models import Item_Model
from . forms import ItemForm


# Create your views here.

# Home View
def index_view(request):
    return render(request, 'InventoApp/index.html')


# Create View
def item_create_view(request):
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
    return render(request, 'InventoApp/item_list.html', {'items':items})


# Update View
# Get item by unique identifier = item_id number
def item_update_view(request, item_id):
    item = Item_Model.objects.get(item_id=item_id)
    form = ItemForm(instance=item)
    if request.method == 'POST':
        # Binding form data FROM the request TO the specific & existing item instance -- the second parameter.
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    return render(request, 'InventoApp/item_form.html', {'form':form})


# Delete View
def item_delete_view(request, item_id):
    item = Item_Model.objects.get(item_id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'InventoApp/item_confirm_delete.html', {'item':item})