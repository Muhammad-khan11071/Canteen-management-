"""
FAQ:
1. somehow to create ```date``` (datetime.date object) to pass to ```retrieve_menu_by_date?```
> A. ```date(<year>,<month>,<date>)```

2. how to utilize any function from this file?
> A. in your file, type on top ```import func``` where func is the name of the function you need
"""

# DONE: implement overwriting a date's entry in record.csv if date already exists
# DONE: implement update_master_entry(item_id, updated_fields)
# DONE: implement delete_master_entry(item_id)

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
    """helper to generate next entry ID by looking at existing entries

    * if master file doesn't exist, returns 1 (fresh start)
    """
    if not os.path.exists(MASTER_FILE):
        return 1  # fresh start

    with open(MASTER_FILE, "r") as f:
        reader = csv.DictReader(f)
        ids = [int(entry["id"]) for entry in reader]

    return max(ids, default=0) + 1


def retrieve_master_menu() -> list[dict]:
    """
    return a list of dicts, with each dict representing a menu entry

    * each dict has keys 'id', 'item', 'price', 'category' and 'upvotes'
    """
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        return list(reader)


def retrieve_menu_by_date(for_date: date = date.today()) -> list[dict]:
    """
    * returns list of menu entries, with each entry represented by a dict
    * returns an empty list if the date is invalid

    Args:
        for_date (datetime.date): default is date.today()
    """

    fmt_date = for_date.strftime(r"%d-%m-%y")

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
            # empty list if no ids found for the date
            return []

    menu_list = []

    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for entry in reader:
            if entry["id"] in ids:
                menu_list.append(entry)

        return menu_list


def retrieve_record() -> list[dict]:
    """
    return a list of dicts, with each dict representing a record entry

    * each dict has keys 'date' and 'item_ids'
    """
    with open(RECORD_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        return list(reader)


def write_to_file(filename: str, fieldnames: str, data: list[dict]) -> None:
    """
    writes given data to given CSV file

    Args:
        filename (str): name of the file (most probably either RECORD_FILE or MASTER_FILE)
        fieldnames (str): name of the fields (most probably either RECORD_FIELDNAMES or MASTER_FIELDNAMES)
        data (list): ```list``` of ```dict```(s) containing entries to write to the file. Each dict should have
        all the keys in ```fieldnames```
    """

    # to avoid data loss, we first write the data to a temporary file and then
    # replace the original one with it after a successful write

    temp_filename = f"{filename}__temp"

    with open(temp_filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    os.replace(temp_filename, filename)
    print(f"Wrote to {filename} successfully!")


def add_entry_to_master_menu(entry_dict: dict) -> None:
    """
    adds a new entry to the master menu

    Args:
        entry_dict (dict): dict with keys 'item', 'price' and 'category'
    """
    data = retrieve_master_menu()

    # checking prior existence
    for item in data:
        if item["item"] == entry_dict["item"] and \
           int(item["price"]) == int(entry_dict["price"]) and \
           item["category"] == entry_dict["category"]:
            print("Item already exists. Not saving ts")
            return

    entry_dict["id"] = generate_new_id()
    entry_dict["upvotes"] = 0

    data.append(entry_dict)

    write_to_file(MASTER_FILE, MASTER_FIELDNAMES, data)


def add_entry_to_record(entry_dict: dict) -> None:
    """
    adds a new entry to the record

    Args:
        entry_dict (dict): dict with keys ```date``` and ```item_ids```
        where ```date``` is a ```datetime.date``` instance and ```item_ids``` is
        a string with space separated menu item IDs
    """
    data = retrieve_record()

    try:
        if entry_dict["date"]:
            entry_dict["date"] = entry_dict["date"].strftime(r"%d-%m-%y")
        else:
            raise KeyError
    except KeyError:
        entry_dict["date"] = date.today().strftime(r"%d-%m-%y")

    entry_dict["item_ids"] = entry_dict["item_ids"].strip()

    over_written = False
    for entry in data:
        if entry["date"] == entry_dict["date"]:
            print(f"overwriting {entry_dict['date']}")
            entry["item_ids"] = entry_dict["item_ids"]
            over_written = True
            break

    if not over_written:
        data.append(entry_dict)

    write_to_file(RECORD_FILE, RECORD_FIELDNAMES, data)


def delete_item(id: int|str) -> None:
    """
    deletes an item from the master menu (hard delete)

    Args:
        id: ID of the item to delete
    """
    data = retrieve_master_menu()

    for item in data:
        if int(item["id"]) == int(id):
            data.remove(item)
            write_to_file(MASTER_FILE, MASTER_FIELDNAMES, data)
            print(f"item of ID: {id} deleted successfully!")

            break
    else:
        print(f"no item of ID: {id} found.")


if __name__ == "__main__":
    # all testing of this file's code to be done here

    # add_entry_to_record(
    #     {
    #         'date': date(2024, 2, 29),
    #         'item_ids': '2 4 5 6 '
    #     }
    # )
    
    # for item in retrieve_record():
    #     for key, val in item.items():
    #         print(f"{key: ^13} {val:^13}", end='')
    #     print()
    
    pass