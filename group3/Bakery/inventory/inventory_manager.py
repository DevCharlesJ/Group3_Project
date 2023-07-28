import sys, os, csv

this_dir = os.path.dirname(__file__)
project_dir = "\\".join(this_dir.split("\\")[:-2]) # Project directory is 2 directories back from this_dir

sys.path.append(project_dir) # Add project path to sys.paths
os.environ['DJANGO_SETTINGS_MODULE'] = 'group3.settings' # then set the 'DJANGO_SETTINGS_MODULE' env variable for django to work

import django
django.setup()
from Bakery.models import Product, Product_Type


CAKES_FILE = os.path.join(this_dir, "cakes.csv")
COOKIES_FILE = os.path.join(this_dir, "cookies.csv")
PRODUCT_TYPES_FILE = os.path.join(this_dir, "product_types.csv")




def read_csv(fp:str) -> list[list]:
    """Returns row data of the given .csv file"""

    read_data = []

    def to_datatypes(row_data:list[str]) -> list:
        formatted = []
        for data in row_data:
            try:
                formatted.append(float(data)) # try to append float conversion
            except:
                formatted.append(data) # append string

        return formatted

    with open(fp, "r") as f:
        for row in csv.reader(f):
            # Append appropriately formatted data
            read_data.append(to_datatypes(row))

    return read_data



def import_product_types(save_instances=True):
    '''loads data from product_types_file into db (if save_instances)
        Expected headers/order:
            name
    '''

    for row_data in read_csv(PRODUCT_TYPES_FILE)[1:]:
        instance = Product_Type(name=row_data[0])
        if save_instances:
            instance.save()
        
        print("Imported:", instance.name, "(SAVED)" if save_instances else "(NOT SAVED)")

def import_products(file, save_instances=True):
    '''loads data from a products file into db (if save_instances)
        Expected headers/order:
            name, price, description
    '''

    product_count = Product.objects.count()
    for row_data in read_csv(file)[1:]:
        name, price, description = row_data

        instance = Product(
            id=product_count,
            name=name,
            price=price,
            description=description
        )

        print(product_count)
        if save_instances:
            instance.save()
        
        product_count += 1 # increment count
        print("Imported:", instance.name, "(SAVED)" if save_instances else "(NOT SAVED)")



# IMPORTS
# import_product_types() # LAST IMPORT 7/28/2023 12:51 PM

# import_products(CAKES_FILE) # LAST IMPORT 7/28/2023 2:05 PM
# import_products(COOKIES_FILE) # LAST IMPORT 7/28/2023 2:10 PM
