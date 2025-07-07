import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from api.models import User, Item, List, ListItem, Membership, PriceItemInfo, Brand, Store

import builtins # cause I repeatedly named variables 'list'

# creates some instances
class Command(BaseCommand):
    help = 'Creates application data'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Reset the DB before populating')

    def handle(self, *args, **kwargs):


        # in case prior data is not wanted, clears out all models' objects
        if kwargs['reset']:
            print("Since reset-flag is set, DB will be reset(including Users)!")
            User.objects.all().delete()
            Item.objects.all().delete()
            Brand.objects.all().delete()
            Store.objects.all().delete()
            List.objects.all().delete()
            Membership.objects.all().delete()
            ListItem.objects.all().delete()
            PriceItemInfo.objects.all().delete()

        # CREATE SUPERUSER
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='test')
            print("!!! Added SUPERUSER 'admin' with pw 'test' !!!")
        
        # CREATE (normal) USER OBJECTS, all with display_name=username
        added = 0
        duplicates = 0
        user_names = ["Test&User1", "JOHN DOE", "Jane Täü-öst&", "DAVE", "Tim", "John@Carlos", "Generic_Username",]
        test_pwd = "test"
        for user_name in user_names:
            user, created = User.objects.get_or_create(username= user_name, defaults={'display_name': user_name})
            if created:
                print(f"Added User: {user.username}!")
                user.set_password(test_pwd)
                user.save()
                added +=1
            else:
                duplicates +=1
        users = User.objects.all()
        print(f"Users added: {added}, Duplicates: {duplicates}, total number: {len(users)}!")


        # CREATE STORE OBJECTS
        added = 0
        duplicates = 0
        store_names = ["Test&Store1", "REWE", "Täü-öst&", "ALDI NORD", "ALDI SÜD", "LIDL", "Generic_Store",]
        
        for store_name in store_names:
            store, created = Store.objects.get_or_create(name= store_name, defaults={'logo': "generic_logo.png"})
            if created:
                print(f"Added store: {store.name}!")
                added +=1
            else:
                duplicates +=1
        stores = Store.objects.all()
        print(f"Stores added: {added}, Duplicates: {duplicates}, total number: {len(stores)}!")

     
        # CREATE BRAND OBJECTS
        added = 0
        duplicates = 0
        brand_names = ["Test&Brand1", "Ja!", "Täü-öst%", "Rittersport", "Müller Milch", "Barilla", "Generic_Brand",]
        
        for brand_name in brand_names:
            brand, created = Brand.objects.get_or_create(name= brand_name, defaults={'logo': "generic_logo.png"})
            if created:
                print(f"Added brand: {brand.name}!")
                added +=1
            else:
                duplicates +=1
        brands = Brand.objects.all()
        print(f"Brands added: {added}, Duplicates: {duplicates}, total number: {len(brands)}!")


        # CREATE ITEM OBJECTS
        added = 0
        duplicates = 0
        item_names = ["Test&Item1", "Penne(Pasta)", "Täü-öst%", "Toast", "Müller Milch Banane", "Kochschinken", "Generic_Item",]
        
        for item_name in item_names:
            item, created = Item.objects.get_or_create(
                name= item_name, 
                brand = random.choice(brands),
                store = random.choice(stores),
                defaults={}
                )
            if created:
                print(f"Added item: {item})!")
                added +=1
            else:
                duplicates +=1
        items = Item.objects.all()
        print(f"Items added: {added}, Duplicates: {duplicates}, total number: {len(items)}!")


        # CREATE LIST OBJECTS
        added = 0
        duplicates = 0
        list_names = ["Test&List1", "GroceryItems", "Einkaufsliste von Täü-öst%", "Shopping list", "Einkaufs- & Todoliste", "Einkauf@43.Woche", "Generic_List",]
        
        for list_name in list_names:
            list, created = List.objects.get_or_create(
                name= list_name, 
                creator= random.choice(users),
                defaults={}
                )
            if created:
                print(f"Added List: {list}!")
                added +=1
            else:
                duplicates +=1
        lists = List.objects.all()
        print(f"Lists added: {added}, Duplicates: {duplicates}, total number: {len(lists)}!")


        # CREATE MEMBERSHIP OBJECTS, intermediary for the ManyToMany Relation between Lists and Users
        added = 0
        duplicates = 0

        # go through all lists
        for list in lists:

            # take a random number of random users to be members of the given list (other than its creator)
            potential_members = User.objects.exclude(id= list.creator.pk)
            member_number = random.randrange(len(potential_members))
            chosen_members = random.sample(builtins.list(potential_members), member_number)

            # create actual membership objects for all chosen members
            for chosen_member in chosen_members:
                membership, created = Membership.objects.get_or_create(
                    joined_list= list,
                    member= chosen_member,
                    defaults={
                        'inviter': list.creator,
                    }
                )
                if created:
                    print(f"Added Membership with {membership}!")
                    added +=1
                else:
                    duplicates +=1
            print(f"Added or got {member_number} members to list: {list}")
        memberships = Membership.objects.all()
        print(f"Memberships added: {added}, Duplicates: {duplicates}, total number: {len(memberships)}!") 


        # CREATE LISTITEM OBJECTS, intermediary for the ManyToMany Relation between Lists and Items
        added = 0
        duplicates = 0

        # go through all lists
        for list in lists:

            # take a random number of random items to be elements of the given list
            rand_item_number = random.randrange(len(items))
            chosen_items = random.sample(builtins.list(items), rand_item_number)

            # create actual ListItem objects for all chosen items
            for chosen_item in chosen_items:
                list_item, created = ListItem.objects.get_or_create(
                    list= list,
                    item= chosen_item,
                    defaults={
                        'amount': random.randrange(1000),
                        'price_total': random.randrange(100),
                        'created_by': pick_creator_for_list_item(list),
                        'description': "This is a TEST ListItem!",
                    }
                )
                if created:
                    print(f"Added ListItem with {list_item}!")
                    added +=1
                else:
                    duplicates +=1
            print(f"Added or got {rand_item_number} ListItems for list: {list}")
        list_items = ListItem.objects.all()
        print(f"ListItems added: {added}, Duplicates: {duplicates}, total number: {len(list_items)}!") 



        # CREATE PRICEITEMINFO OBJECTS, intermediary for the ManyToMany Relation between Lists and Items (maybe add manual dates for better testing?)
        added = 0
        duplicates = 0

        # go through all items
        for item in items:
            # create up to 5 PriceItemInfo objects for the given item
            x = random.randrange(5)
            for i in range(x):
                price_info, created = PriceItemInfo.objects.get_or_create(
                    item= item,
                    price_per_1_unit = Decimal(random.randrange(1000)),
                    defaults={}
                )
                if created:
                    print(f"Added PriceItemInfo with {price_info}!")
                    added +=1
                else:
                    duplicates +=1
            print(f"Added or got {x} Priceinfos for Item: {item}")
        price_item_infos = PriceItemInfo.objects.all()
        print(f"PriceItemInfo added: {added}, Duplicates: {duplicates}, total number: {len(price_item_infos)}!") 



# helper method for choosing the creator when creating testobjects for ListItem. If the given list has members, return one at random, 
# else, if it exists, return the list creator and, if even that is not possible, return the superuser called admin, previously created in this script
def pick_creator_for_list_item(given_list: List) ->User:
    members = list(given_list.members.all())
    if members:
        return random.choice(members)
    if given_list.creator is not None:
        return given_list.creator
    return User.objects.filter(username='admin').first()
