from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view ,name='index'),
    path('create/', views.item_create_view ,name='item_create'),
    path('list/', views.item_list_view ,name='item_list'),
    path('update/<int:item_id>/', views.item_update_view ,name='item_update'),
    path('delete/<int:item_id>/', views.item_delete_view ,name='item_delete'),
]
