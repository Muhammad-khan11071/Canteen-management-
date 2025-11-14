import csv
import datetime 
from datetime import date
from data_manager import retrieve_master_menu, retrieve_menu_by_date  # import your existing function
from data_manager import retrieve_menu_by_date

def filter_menu_by_item( value: str, for_date: date = date.today()) -> list[dict]:
    """
    Filters menu items for a given date based on a specific column and value.
    Supports both categorical and numerical comparisons.

    args:
        date (date): The date to retrieve the menu for.
        column (str): Column name to filter by.
        value (str): Value to match in the filter column.
        operator (str): Comparison operator for numeric columns ('>', '<', '>=', '<=', '==').

    Returns:
        list[dict]: Filtered list of menu entries for the given date.
    """
    
    menu_by_date = retrieve_menu_by_date(for_date)
    if menu_by_date==None or len(menu_by_date)==0:
        print(f"Error: No menu found for date '{for_date}'.")
        return []
    
    # Filter logic
    filtered_rows = []
    
    filtered_rows = [
        item for item in menu_by_date
        if str(item['category']).strip().lower() == str(value).strip().lower()
    ]
    
    print(f"Successfully Filtered menu based on item and value {value}")
    return filtered_rows

def filter_menu_by_price(min , max, for_date: date = date.today()) -> list[dict]:
    """
    Filters menu items for a given date based on a specific column and value.
    Supports both categorical and numerical comparisons.

    args:
        date (date): The date to retrieve the menu for.
        column (str): Column name to filter by.
        value (str): Value to match in the filter column.
        operator (str): Comparison operator for numeric columns ('>', '<', '>=', '<=', '==').

    Returns:
        list[dict]: Filtered list of menu entries for the given date.
    """
    
    menu_by_date = retrieve_menu_by_date(for_date)
    
    if menu_by_date==None or len(menu_by_date)==0:
        print(f"Error: No menu found for date '{date}'.")
        return []

    # Filter logic
    filtered_rows = []
    price_Range = range(min,max+1)
    for item in menu_by_date:
        item_price = float(item['price'])
        if item_price in price_Range:
            filtered_rows.append(item)
    print(f"Filtered menu based on price column and range {min} - {max}")
    return filtered_rows

def sort_menu(column, descending=False):
    master_menu = retrieve_master_menu()
    
    if not master_menu:
        print("Error: Master menu is empty or could not be loaded.")
        return []

    # Validate that the column exists
    if column not in master_menu[0]:
        print(f"Error: Column '{column}' not found in master menu.")
        return []
    
    def sort_key(menu_row):
        try :
            return float(menu_row[column])
        except ValueError:
            return str(menu_row[column]).lower()
    master_menu.sort(key= sort_key, reverse=descending)     # , reverse=True for descending
    
    print(f'Successfully sorted by {column}')
    return master_menu

def search_menu_by_item(query,master_menu):
    column='item'
    # Base Case
    if len(master_menu)==0:
        return []
    else:
        first_row = master_menu[0]
        if query.lower() in first_row[column].lower():
            return  [first_row] + search_menu_by_item(query,master_menu[1:]) 
        else:
            return search_menu_by_item(query,master_menu[1:])

# Testing
filtered_menu = filter_menu_by_item('fast food',datetime.date(2025,11,7))

for row in filtered_menu:
    print(row)
    
    
filtered_menu2 = filter_menu_by_price(200, 300,datetime.date(2025,11,7))

for row in filtered_menu2:
    print(row)

print('--------------------------------------------------------------------')

sorted_menu = sort_menu('item')
for row in sorted_menu:
    print(row['item'])
    
    print('----------------------------------------------------------')

    
sorted_menu = sort_menu('price',descending=True)
for row in sorted_menu:
    print(row)

print('----------------------------------------------------------')

search_results = search_menu_by_item('b',retrieve_master_menu())
for row in search_results:
    print(row)