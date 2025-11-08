import csv
from data_manager import retrieve_master_menu  # import your existing function

def filter_categorical(column, value) -> list[dict]:
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

def filter_numerical(column, operator, value) -> list[dict]:
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
    valid_operators = {'equal to','greater than','less than'}
    if operator.lower() not in valid_operators:
        print(f"Error: Invalid operator '{operator}'. Use one of {valid_operators}.")
        return []
    
    

    # Filter items (case-insensitive and trims spaces)
    filtered_rows=[]
    if operator.lower()=='equal to':
        filtered_rows = [
            item for item in master_menu
            if float(item[column]) == float(value)
        ]
    elif operator.lower()=='greater than':
        filtered_rows = [
            item for item in master_menu
            if float(item[column]) > float(value)
        ]
    else:
        filtered_rows = [
            item for item in master_menu
            if float(item[column]) < float(value)
        ]

    return filtered_rows

# Testing
filtered_menu = filter_numerical('price','equal to',250)

for row in filtered_menu:
    print(row)