from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import ItemSerializer, BrandSerializer, StoreSerializer, ListItemSerializer, PriceItemInfoSerializer, ListSerializer, ListSerializer_detailed
from api.models import List, Item, Brand, Store, User, ListItem, Membership, PriceItemInfo

# view method for returning ALL current instances of the Item model as Json 
@api_view(['GET'])
def all_items(request):
    items = Item.objects.prefetch_related('brand', 'store')
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

# view method for returning a specific instance of the Item model as Json 
@api_view(['GET'])
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

# view method for returning ALL current instances of the Store model as Json 
@api_view(['GET'])
def all_stores(request):
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)

# view method for returning ALL current instances of the Brand model as Json 
@api_view(['GET'])
def all_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

# view method for returning ALL current instances of the PriceItemInfo model as Json 
@api_view(['GET'])
def all_price_infos(request):
    price_infos = PriceItemInfo.objects.prefetch_related('item__brand', 'item__store')
    serializer = PriceItemInfoSerializer(price_infos, many=True)
    return Response(serializer.data)

# view method for returning all price infos for the given item
@api_view(['GET'])
def price_infos_for_item(request, item_id):
    price_infos = PriceItemInfo.objects.filter(item_id = item_id)
    serializer = PriceItemInfoSerializer(price_infos, many=True)
    return Response(serializer.data)

# view method for returning all lists
@api_view(['GET'])
def all_lists(request):
    lists = List.objects.all()
    serializer = ListSerializer(lists, many=True)
    return Response(serializer.data)

# view method for returning a specific instance of the List model as Json 
# different from the all_lists view, this also displays each member and item of the list(rather than just the count)
@api_view(['GET'])
def list_detail(request, list_id):
    given_list = get_object_or_404(List, pk=list_id)
    serializer = ListSerializer_detailed(given_list)
    return Response(serializer.data)


# for ListItem
# TODO: Return only those LISTitems, a user is allowed to view(requires changes to the model!)