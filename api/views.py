from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from api.serializers import ItemSerializer, BrandSerializer, StoreSerializer, ListItemSerializer, PriceItemInfoSerializer, ListSerializer, ListSerializer_detailed
from api.models import List, Item, Brand, Store, User, ListItem, Membership, PriceItemInfo

# view class for returning ALL current instances of the Item model as Json 
class AllItemsAPIView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.prefetch_related('brand', 'store')

# view class for returning a specific instance of the Item model as Json 
class ItemDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.prefetch_related('brand', 'store')

# view class for returning ALL current instances of the Store model as Json 
class AllStoresAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.all()

# view class for returning ALL current instances of the Brand model as Json 
class AllBrandsAPIView(generics.ListAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        return Brand.objects.all()

# view class for returning ALL current instances of the PriceItemInfo model as Json 
class AllPriceInfosAPIView(generics.ListAPIView):
    serializer_class =PriceItemInfoSerializer

    def get_queryset(self):
        return PriceItemInfo.objects.prefetch_related('item__brand', 'item__store')

# view class for returning all price infos for the given item
class PriceInfosForItemView(generics.ListAPIView):
    serializer_class = PriceItemInfoSerializer

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return PriceItemInfo.objects.filter(item_id=item_id).prefetch_related('item')

# view class for returning all lists
class AllListsAPIView(generics.ListAPIView):
    serializer_class = ListSerializer

    def get_queryset(self):
        return List.objects.prefetch_related('members', 'items', 'creator')

# view class for returning a specific instance of the List model as Json 
# different from the all_lists view, this also displays each member and item of the list(rather than just the count)
class ListDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ListSerializer_detailed

    def get_queryset(self):
        return List.objects.prefetch_related('list_items__item__store', 'list_items__item__brand', 'list_memberships__member')
    
