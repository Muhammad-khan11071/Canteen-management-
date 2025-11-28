import csv
from data_manager import retrieve_master_menu  # import your existing function

def filter_numerical(column, value) -> list[dict]:
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

# In data_handling2.py

def sort_numerical(data_list, key, order='ascending'):
    """
    Sorts a list of dictionaries based on a numerical key.
    
    Args:
        data_list (list): List of dictionaries (e.g., the menu).
        key (str): The dictionary key to sort by (e.g., 'price').
        order (str): 'ascending' or 'descending'.
        
    Returns:
        list: The sorted list.
    """
    def get_sort_key(item):
        try:
            # Convert to float for proper numerical sorting
            return float(item.get(key, 0))
        except ValueError:
            return 0

    is_reverse = (order == 'descending')
    
    return sorted(data_list, key=get_sort_key, reverse=is_reverse)
# Testing