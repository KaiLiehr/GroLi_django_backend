from django.urls import path
from . import views


urlpatterns = [
    path('items/', views.AllItemsAPIView.as_view(), name='all_items'),
    path('items/<int:pk>/', views.ItemDetailAPIView.as_view(), name='item_detail'),
    path('brands/', views.AllBrandsAPIView.as_view(), name='all_brands'),
    path('stores/', views.AllStoresAPIView.as_view(), name='all_stores'),
    path('prices/', views.AllPriceInfosAPIView.as_view(), name='all_prices'),
    path('prices/<int:item_id>/', views.PriceInfosForItemView.as_view(), name='item_prices'),
    path('lists/', views.AllListsAPIView.as_view(), name='all_lists'),
    path('lists/<int:pk>/', views.ItemDetailAPIView.as_view(), name='list_detail'),
]
