# URLS
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

# issue: reverse_lazy not being read as a function

# User Authentication Feature Imports
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from django.contrib import messages


# CRUD
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormView
from django.db import transaction
from .services import InventoryService


# App Classes
from .models import Item_Model, Lot, Movement
from .forms import ItemForm, UserRegistrationForm, LotForm, StockInForm, StockOutForm


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
            # Collecting all form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{error}")

            # Adding a comprehensive error message
            messages.error(request, "<br>".join(error_messages))

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


# ----------
# CRUD Inventory Feature Views
# ----------

# ----------
# ITEM VIEWS
# ----------


class ItemModelListView(LoginRequiredMixin, ListView):
    model = Item_Model
    template_name = "InventoApp/item_list.html"
    context_object_name = "items"


class ItemModelCreateView(LoginRequiredMixin, CreateView):
    model = Item_Model
    form_class = ItemForm
    template_name = "InventoApp/item_form.html"


class ItemModelDetailView(LoginRequiredMixin, DetailView):
    model = Item_Model
    template_name = "InventoApp/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lots"] = self.object.lots.all()
        context["total_available"] = self.object.get_available_quantity
        return context


class ItemModelUpdateView(LoginRequiredMixin, UpdateView):
    model = Item_Model
    form_class = ItemForm
    template_name = "InventoApp/item_form.html"


class ItemDeleteView(DeleteView):
    model = Item_Model
    template_name = "InventoApp/item_confirm_delete.html"
    success_url = reverse_lazy("item_list")


#  ----------
# MOVEMENT VIEWS
#  ----------


class MovementListView(LoginRequiredMixin, ListView):
    model = Movement
    template_name = 'InventoApp/movement_list.html'
    context_object_name = "movements"
    paginate_by = 20

    def get_queryset(self):
        return Movement.objects.order_by("-date")


class StockInView(LoginRequiredMixin, FormView):
    template_name = "InventoApp/stock_in.html"
    form_class = StockInForm
    success_url = reverse_lazy("stock_in")

    def form_valid(self, form):
        try:
            with transaction.atomic():
                lot, movement = InventoryService.stock_in(
                    item=form.cleaned_data["item"],
                    quantity=form.cleaned_data["quantity"],
                    unit_cost=form.cleaned_data["unit_cost"],
                    performed_by=self.request.user.username,
                    expiry_date=form.cleaned_data.get("expiry_date"),
                    received_date=form.cleaned_data["received_date"],
                    notes=form.cleaned_data.get("notes", ""),
                    # 2nd Param = default value
                )

        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)


class StockOutView(LoginRequiredMixin, FormView):
    template_name = "InventoApp/stock_out.html"
    form_class = StockOutForm
    success_url = reverse_lazy("stock_out")

    def form_valid(self, form):
        try:
            with transaction.atomic():
                movements_created = InventoryService.stock_out(
                    item=form.cleaned_data["item"],
                    quantity=form.cleaned_data["quantity"],
                    notes=form.cleaned_data.get("notes", ""),
                    performed_by=self.request.user.username,
                )
                messages.success(
                    self.request,
                    f"Stock out successful. {len(movements_created)} lots used.",
                )
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)


class MovementDeleteView(DeleteView):
    model = Movement
    template_name = "InventoApp/movement_confirm_delete.html"
    success_url = reverse_lazy("movement_list")


# ----------
# LOT VIEWS
# ----------
class LotListView(ListView):
    model = Lot
    template_name = "InventoApp/lot_list.html"
    context_object_name = "lots"
    paginate_by = 20


class LotUpdateView(LoginRequiredMixin, UpdateView):
    model = Lot
    form_class = LotForm
    template_name = "InventoApp/lot_form.html"


# DELETE VIEWS


class LotDeleteView(DeleteView):
    model = Lot
    template_name = "InventoApp/lot_confirm_delete.html"
    success_url = reverse_lazy("lot_list")


"""
# ITEM
@login_required
def item_delete_view(request, item_id):
    item = Item_Model.objects.get(item_id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect("item_list")
    return render(request, "InventoApp/item_confirm_delete.html", {"item": item})
"""


"""
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



"""
