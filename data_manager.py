"""
FAQ:
1. somehow to create date (datetime.date object) to pass to retrieve_menu_by_date?
> A. date(<year>,<month>,<date>)

2. how to utilize any function from this file?
> A. in your file, type on top import func where func is the name of the function you need
"""

import csv
import os
from datetime import date

# Get the folder where data_manager.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MASTER_FIELDNAMES = ["id", "item", "price", "category", "upvotes"]
RECORD_FIELDNAMES = ["date", "item_ids"]

# Create absolute paths
MASTER_FILE = os.path.join(BASE_DIR, 'master_menu.csv')
RECORD_FILE = os.path.join(BASE_DIR, 'record.csv')


def generate_new_id() -> int:
    """helper to generate next entry ID by looking at existing entries"""
    if not os.path.exists(MASTER_FILE):
        return 1  # fresh start

    with open(MASTER_FILE, "r") as f:
        reader = csv.DictReader(f)
        ids = [int(entry["id"]) for entry in reader]

    return max(ids, default=0) + 1


def retrieve_master_menu() -> list[dict]:
    """return a list of dicts, with each dict representing a menu entry"""
    if not os.path.exists(MASTER_FILE):
        return []
        
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def retrieve_menu_by_date(for_date: date = None) -> list[dict]:
    """returns list of menu entries for a specific date"""
    if for_date is None:
        for_date = date.today()

    fmt_date = for_date.strftime(r"%d-%m-%y")

    if not os.path.exists(RECORD_FILE):
        return []

    with open(RECORD_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        ids = None
        for row in reader:
            if row["date"] == fmt_date:
                ids = row["item_ids"]
                break

        if ids:
            ids = ids.split()
        else:
            return []

    menu_list = []
    
    # Get master data to lookup items
    master_data = retrieve_master_menu()
    
    for entry in master_data:
        if entry["id"] in ids:
            menu_list.append(entry)

    return menu_list


def retrieve_record() -> list[dict]:
    """return a list of dicts, with each dict representing a record entry"""
    if not os.path.exists(RECORD_FILE):
        return []
        
    with open(RECORD_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_to_file(filename:str, fieldnames:str, data: list[dict]) -> None:
    """
    writes given list of ids to the record CSV for the given date
    """
    # --- CRITICAL FIX FOR WINDOWS ---
    # We must separate the folder path from the filename
    directory = os.path.dirname(filename)
    base_name = os.path.basename(filename)
    
    # Create the temp file in the SAME directory, but with a valid name
    temp_filename = os.path.join(directory, f"temp__{base_name}")

    with open(temp_filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    # Replace the original file with the new one
    try:
        os.replace(temp_filename, filename)
        print(f"Wrote to {filename} successfully!")
    except OSError as e:
        print(f"Error renaming file: {e}")


def add_entry_to_master_menu(entry_dict: dict) -> None:
    """adds a new entry to the master menu"""
    data = retrieve_master_menu()

    entry_dict["id"] = generate_new_id()
    entry_dict["upvotes"] = 0

    data.append(entry_dict)

    write_to_file(MASTER_FILE, MASTER_FIELDNAMES, data)


def add_entry_to_record(entry_dict: dict) -> None:
    """
    Adds a new entry to the record. 
    If the date exists, it APPENDS new items to the existing list.
    """
    data = retrieve_record()

    # Ensure date is string formatted (dd-mm-yy)
    if isinstance(entry_dict["date"], date):
        entry_dict["date"] = entry_dict["date"].strftime(r"%d-%m-%y")
    
    found_date = False
    
    for entry in data:
        if entry['date'] == entry_dict['date']:
            print(f"Date found: {entry_dict['date']}. Appending new items...")
            
            # 1. Get existing IDs as a list
            current_ids = entry['item_ids'].split()
            
            # 2. Get the new IDs passed in
            new_ids = entry_dict['item_ids'].split()
            
            # 3. Append only the IDs that are NOT already in the list
            for new_id in new_ids:
                if new_id not in current_ids:
                    current_ids.append(new_id)
            
            # 4. Save back as a space-separated string
            entry['item_ids'] = " ".join(current_ids)
            
            found_date = True
            break
    
    # If date was not found, add it as a new entry
    if not found_date:
        data.append(entry_dict)

    write_to_file(RECORD_FILE, RECORD_FIELDNAMES, data)

if __name__ == "__main__":
    # Testing
    pass