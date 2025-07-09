from rest_framework import serializers
from .models import User, Item, List, ListItem, PriceItemInfo, Brand, Store, Membership

# This file contains the serializer classes to convert instances of the models of the api app to json and vice versa
# TODO: Once all views are created, decide what is really necessary to display/return, until then, just display all nested relations
# TODO: add default sortings either for db or for returned views

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo',)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'logo',)

class ItemSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    store = StoreSerializer()
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'brand',
            'store',
            'measurement',
            'image',
        )

class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = (
            'id',
            'list',
            'item',
            'status',
            'amount',
            'price_total',
            'created_by',
            'created_at',
            'description',
        )

class PriceItemInfoSerializer(serializers.ModelSerializer):
    item = ItemSerializer() # Do I really want to display item details in the prices view?
    class Meta:
        model = PriceItemInfo
        fields = (
            'id',
            'item',
            'price_per_1_unit',
            'date',
        )

    # Better here or better in ListItem? I think here, since this will be the source of the calculated price total and comparisons
    def validate_price_per_1_unit(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0!"
            )
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            # 'username', # omitted cause public only needs display name
            'display_name',
        )

# for view list_detail(): does not display joined_list(redundant) and only displays inviter as id(not full User) for readability
class MembershipSerializer(serializers.ModelSerializer):
    member = UserSerializer()
    #inviter = UserSerializer()
    class Meta:
            model = Membership
            fields = (
                'id',
                #'joined_list',
                'member',
                'inviter',
                'joined_at',
            )

# For view all_lists(), does display a count of both members and items but not the actual members or items
class ListSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    creator = UserSerializer()
    class Meta:
        model = List
        fields = (
            'id',
            'name',
            'item_count', 
            'member_count',
            'creator',
            'created_at',
        )

    def get_item_count(self, obj):
        return obj.items.count() 

    def get_member_count(self, obj):
        return obj.members.count()

# for view list_detail(), displays both members and items
class ListSerializer_detailed(serializers.ModelSerializer):
    creator = UserSerializer()
    list_memberships = MembershipSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = (
            'id',
            'name',
            'creator',
            'created_at',
            'list_memberships',
        )
    
