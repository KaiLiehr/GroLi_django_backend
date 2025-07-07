from django.urls import path
from . import views


urlpatterns = [
    path('items/', views.all_items, name='all_items'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('brands/', views.all_brands, name='all_brands'),
    path('stores/', views.all_stores, name='all_stores'),
]
