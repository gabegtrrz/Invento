from django.shortcuts import render, redirect

# User Authentication Feature Imports
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# App Classes
from .models import Item_Model
from .forms import ItemForm, UserRegistrationForm


# Create your views here.


# Home View
def index_view(request):
    return render(request, "InventoApp/index.html")


# User Authentication Feature Views


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # becomes a User object/instance
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect("item_list")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("item_list")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Logged out successfully.")
        return redirect("login")


# CRUD Inventory Feature Views


# Create View
@login_required
def item_create_view(request):
    # this is where we want to instantiate/create an item RECORD/Object,
    # or facilitate its creation by providing the form to the user.

    form = ItemForm()

    # Logic when POST
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("item_list")

    # Logic to render the FORM for filling it up
    # Remember that Django Views handle the logic.
    else:
        return render(request, "InventoApp/item_form.html", {"form": form})


# Read View
@login_required
def item_list_view(request):
    items = Item_Model.objects.all()
    return render(request, "InventoApp/item_list.html", {"items": items})


# Update View
# Get item by unique identifier = item_id number
@login_required
def item_update_view(request, item_id):
    item = Item_Model.objects.get(item_id=item_id)
    form = ItemForm(instance=item)
    if request.method == "POST":
        # Binding form data FROM the request TO the specific & existing item instance -- the second parameter.
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    return render(request, "InventoApp/item_form.html", {"form": form})


# Delete View
@login_required
def item_delete_view(request, item_id):
    item = Item_Model.objects.get(item_id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect("item_list")
    return render(request, "InventoApp/item_confirm_delete.html", {"item": item})
