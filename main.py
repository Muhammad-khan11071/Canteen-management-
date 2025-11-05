import csv
import os

FIELDNAMES = ['id', 'item', 'price', 'category']


def generate_new_id(filename='menu.csv'):
    """helper to generate next entry ID by looking at existing records"""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, fieldnames=FIELDNAMES)
        ids = [int(item['id']) for item in reader]
        
    return max(ids, default=0)+1


def retrieve_menu(filename='menu.csv'):
    """yields each menu entry from the csv"""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, fieldnames=FIELDNAMES)
        for row in reader:
            yield row

def add_menu_entry(filename='menu.csv'):
    """takes entry data and saves it to the csv"""

    entry_dict = {'id': generate_new_id()}
    for field in FIELDNAMES:
        if field != 'id':
            entry_dict[field] = input(f'Enter {field.capitalize()}: ')

    temp_filename = f'temp__{filename}'

    with open(temp_filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        existing_data = retrieve_menu()

        for entry in existing_data:
            writer.writerow(entry)
        
        writer.writerow(entry_dict)
    
    os.replace(temp_filename, filename)
    print('Entry added successfully!')


if __name__ == '__main__':
    add_menu_entry()

    for entry in retrieve_menu():
        for key, value in entry.items():
            print(f"{key} = {value}")
        print()