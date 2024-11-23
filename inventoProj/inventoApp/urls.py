from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),

    # USER AUTHENTICATION FEATURE
    
    path("login/", views.login_view, name="login"),

    path("register/", views.register_view, name="register"),

    path("logout/", views.logout_view, name="logout"),

    # ITEM_MODEL URLS

    path('item_list/', views.ItemModelListView.as_view(), name='item_list'),

    path('item/new/',views.ItemModelCreateView.as_view(),name='item_create'),

    path("item/<int:pk>/", views.ItemModelDetailView.as_view(), name="item_detail"),

    path("item/<int:pk>/edit/", views.ItemModelUpdateView.as_view(), name="item_update"),

    path("item/<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),

    # MOVEMENT URLS
    path("movement_list/", views.MovementListView.as_view(), name="movement_list"),

    path('stock-in/', views.StockInView.as_view(), name='stock_in'),

    path('stock-out/', views.StockOutView.as_view(), name='stock_out'),

    path("movement/<int:pk>/delete", views.MovementDeleteView.as_view(), name="movement_delete"),

    # LOT URLS
    path("lot-list/", views.LotListView.as_view(), name="lot_list"),

    path("lot/<int:pk>/edit/", views.LotUpdateView.as_view(), name="lot_update"),

    path("lot/<int:pk>/delete/", views.LotDeleteView.as_view(), name="lot_delete"),
]
    
    # path("create/", views.item_create_view, name="item_create"),
    # path("list/", views.item_list_view, name="item_list"),
    # path("update/<int:item_id>/", views.item_update_view, name="item_update"),
    # path("delete/<int:item_id>/", views.item_delete_view, name="item_delete"),
    