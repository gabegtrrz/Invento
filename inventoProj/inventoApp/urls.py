from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    # User Authentication Feature
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    # CRUD Inventory Tracking Feature
    path("create/", views.item_create_view, name="item_create"),
    path("list/", views.item_list_view, name="item_list"),
    path("update/<int:item_id>/", views.item_update_view, name="item_update"),
    path("delete/<int:item_id>/", views.item_delete_view, name="item_delete"),
]
