from django.urls import path
from . import views


urlpatterns = [
    path('items/', views.all_items, name='all_items'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('brands/', views.all_brands, name='all_brands'),
    path('stores/', views.all_stores, name='all_stores'),
    path('prices/', views.all_price_infos, name='all_prices'),
    path('prices/<int:item_id>/', views.price_infos_for_item, name='item_prices'),
    path('lists/', views.all_lists, name='all_lists'),
    #path('lists/<int:list_id>/', views.list_detail, name='list_detail'),
]
