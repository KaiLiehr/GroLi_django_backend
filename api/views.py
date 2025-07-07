from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import ItemSerializer, BrandSerializer, StoreSerializer
from api.models import Item, Brand, Store

# view method for returning ALL current instances of the Item model as Json 
@api_view(['GET'])
def all_items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
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

# view method for returning a specific instance of the Item model as Json 
@api_view(['GET'])
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)


# for ListItem
# TODO: Return only those LISTitems, a user is allowed to view(requires changes to the model!)