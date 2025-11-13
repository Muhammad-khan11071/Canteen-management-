import csv
from datetime import datetime
from datetime import date
from data_manager import retrieve_master_menu, retrieve_menu_by_date  # import your existing function

def filter_categorical(column: str, value: str) -> list[dict]:
    """
    Filters rows from master menu based on a specific column and value,
    and returns a list of dictionaries (each representing a filtered row).

    Parameters:
        column (str): Column name to filter by.
        value (str): Value to match in the filter column.

    Returns:
        list[dict]: List of filtered menu entries.
    """

    # Retrieve all menu data from data_manager
    master_menu = retrieve_master_menu()

    if not master_menu:
        print("Error: Master menu is empty or could not be loaded.")
        return []

    # Validate that the column exists
    if column not in master_menu[0]:
        print(f"Error: Column '{column}' not found in master menu.")
        return []

    # Filter items (case-insensitive and trims spaces)
    filtered_rows = [
        item for item in master_menu
        if str(item[column]).strip().lower() == str(value).strip().lower()
    ]

    return filtered_rows

def filter_numerical(column:str, value:int, operator:str = '==') -> list[dict]:
    """
    Filters rows from master menu based on a specific column and value,
    and returns a list of dictionaries (each representing a filtered row).

    Parameters:
        column (str): Column name to filter by.
        value (str): Value to match in the filter column.

    Returns:
        list[dict]: List of filtered menu entries.
    """

    # Retrieve all menu data from data_manager
    master_menu = retrieve_master_menu()

    if not master_menu:
        print("Error: Master menu is empty or could not be loaded.")
        return []

    # Validate that the column exists
    if column not in master_menu[0]:
        print(f"Error: Column '{column}' not found in master menu.")
        return []
    
    # Validate operator:
    valid_operators = {'==','>','<','>=','<='}
    if operator not in valid_operators:
        print(f"Error: Invalid operator '{operator}'. Use one of {valid_operators}.")
        return []
    
    

    # Filter items (case-insensitive and trims spaces)
    filtered_rows=[]
    for item in master_menu:
        try:
            item_val = float(item[column])
            target_val = float(value)
            if eval(f"item_val {operator} target_val"):
                filtered_rows.append(item)
        except ValueError:
            continue

    return filtered_rows

from data_manager import retrieve_menu_by_date

def filter_menu_by_date(date: date, column: str, value: str, operator: str = "==") -> list[dict]:
    """
    Filters menu items for a given date based on a specific column and value.
    Supports both categorical and numerical comparisons.

    Parameters:
        date (str): The date to retrieve the menu for.
        column (str): Column name to filter by.
        value (str): Value to match in the filter column.
        operator (str): Comparison operator for numeric columns ('>', '<', '>=', '<=', '==').

    Returns:
        list[dict]: Filtered list of menu entries for the given date.
    """
    
    if isinstance(date, str):
        try:
            date_input = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in 'YYYY-MM-DD' format")
    
    menu_by_date = retrieve_menu_by_date(date_input)
    
    if menu_by_date==None or len(menu_by_date)==0:
        print(f"Error: No menu found for date '{date}'.")
        return []

    if column not in menu_by_date[0]:
        print(f"Error: Column '{column}' not found in menu data for date '{date}'.")
        return []

    # Try to detect if the column is numeric
    is_numeric = False
    try:
        float(menu_by_date[0][column])
        is_numeric = True
    except (ValueError, TypeError):
        pass

    # Filter logic
    filtered_rows = []
    if is_numeric:
        valid_operators = {'==','>','<','>=','<='}
        if operator not in valid_operators:
            print(f"Error: Invalid operator '{operator}'. Use one of {valid_operators}.")
            return []

        for item in menu_by_date:
            try:
                item_val = float(item[column])
                target_val = float(value)
                if eval(f"item_val {operator} target_val"):
                    filtered_rows.append(item)
            except ValueError:
                continue
    else:
        filtered_rows = [
            item for item in menu_by_date
            if str(item[column]).strip().lower() == str(value).strip().lower()
        ]

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
filtered_menu = filter_numerical('price',250,'>=')

#for row in filtered_menu:
 #   print(row)
    
    
filtered_menu2 = filter_menu_by_date('2025-11-7','price',250,'>=')

for row in filtered_menu2:
    print(row)

print('--------------------------------------------------------------------')

sorted_menu = sort_menu('item')
for row in sorted_menu:
    print(row['item'])
    
search_results = search_menu_by_item('GER',retrieve_master_menu())
for row in search_results:
    print(row)