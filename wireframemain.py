import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import date
import os

# --- importing functions from data_managing files ---
from data_manager import (
    add_entry_to_master_menu,
    retrieve_master_menu,
    add_entry_to_record,
    retrieve_menu_by_date,
    delete_item,
)
from data_handling import filter_numerical, sort_numerical

# --- GLOBAL VARIABLES ---
current_dir = os.path.dirname(os.path.abspath(__file__))  # used to put relative paths
records = []  # temporary list to store items for today's menu

# -------------------------
# function defs
# -------------------------


def add_ent(state, item_id):
    """
    handles checking and unchecking of items
    """
    value = state.get()
    str_id = str(item_id)

    if value == 1:
        if str_id not in records:
            records.append(str_id)
    else:
        if str_id in records:
            records.remove(str_id)

    print(f"sleected Ids: {records}")


def del_ent(frame, name):
    """
    Deletes items from Main mneu
    """
    if messagebox.askyesno(
        "Delete Item", f"Are you sure you want to remove '{name}' from this view?"
    ):
        frame.destroy()
        print(f"following item deleted {name}")
        return 1
    return 0


def del_item(ID, frame, name):
    """
    Deletes item from the master list of all items AND !!!deletes then entry from the menu CSV!!!
    """
    if del_ent(frame, name):
        delete_item(ID)


def create_item_frame(parent, record, show_checkbox=True):
    """
    this helper function creates item frames and returns them
    """
    item = record
    frame = ttk.Frame(parent, padding=10, relief="solid", width=500)

    # defining columns and their weights
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=0)
    frame.columnconfigure(2, weight=1)

    # --- Image Handling ---
    image_path = os.path.join(current_dir, "static", "images", f"{item['id']}.jpeg")
    default_image_path = os.path.join(current_dir, "static", "images", "default.jpg")

    photo = None
    try:
        # Try specific ID image
        if os.path.exists(image_path):
            img_obj = Image.open(image_path)
        # Try default image
        elif os.path.exists(default_image_path):
            img_obj = Image.open(default_image_path)
        else:
            img_obj = None

        if img_obj:
            img_obj = img_obj.resize((150, 100))
            photo = ImageTk.PhotoImage(img_obj)

    except Exception as e:
        print(f"Error loading image: {e}")

    # Image Label
    img_label = ttk.Label(frame, relief="ridge", width=20)
    if photo:
        img_label.config(image=photo)
        img_label.image = photo
    else:
        img_label.config(text="No Image", anchor="center")
    img_label.grid(row=0, column=0, rowspan=4, padx=5, pady=5)

    # setting item's values
    ttk.Label(frame, text=f"Price: {item['price']}", font=("Arial", 10, "bold")).grid(
        row=0, column=2, sticky="w"
    )
    ttk.Label(frame, text=item["item"], font=("Arial", 12)).grid(
        row=1, column=2, sticky="w"
    )
    ttk.Label(frame, text=f"Category: {item['category']}").grid(
        row=2, column=2, sticky="w"
    )

    # --- Checkbox Logic ---
    if show_checkbox:
        check_var = tk.IntVar()
        if str(item["id"]) in records:
            check_var.set(1)
        checkbox = tk.Checkbutton(
            frame,
            text="Add to Today",
            variable=check_var,
            command=lambda: add_ent(check_var, item["id"]),
        )
        checkbox.grid(row=3, column=2, sticky="w")

    # --- Delete/Remove Button Logic ---
    # Moved OUTSIDE the show_checkbox block so buttons still appear on the right side
    if parent == right_scrollable_frame:
        # Button for Today's Menu (Removes from view)
        delbt = tk.Button(
            frame,
            text="—",
            font=("Arial", 10, "bold"),
            command=lambda: del_ent(frame, item["item"]),
            bg="orange", # Changed to orange to distinguish from permanent delete
            fg="white",
        )
        delbt.grid(row=0, column=3, padx=10, sticky="e")
    else:
        # Button for Master Menu (Permanently deletes item)
        delbt = tk.Button(
            frame,
            text="X",
            font=("Arial", 10, "bold"),
            command=lambda: del_item(item["id"], frame, item["item"]),
            bg="red",
            fg="white",
        )
        delbt.grid(row=0, column=3, padx=10, sticky="e")

    return frame


# -------------------------
# Button Commands
# -------------------------


def on_search():
    """Filters the main menu by name and resets sort options"""
    
    # 1 Reset Dropdown to Default
    selected_option.set("Show All")

    # 2 Hide Price Filter 
    price_label.pack_forget()
    price_entry_hidden.pack_forget()
    apply_filter_btn.pack_forget()

    # 3. Existing Search Logic
    query = search_entry.get().lower().strip()

    # Clear current view
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
        
    # Get data
    all_items = retrieve_master_menu()
    found = False
    for item in all_items:
        # Search in Name 
        if query in item["item"].lower():
            create_item_frame(scrollable_frame, item).pack(fill="x", pady=5)
            found = True

    if not found:
        ttk.Label(scrollable_frame, text="No items found.").pack(pady=10)


def on_update():
    """
    Sends selected items to records.csv by merging new items with existing ones.
    """
    if not records:
        messagebox.showwarning("Warning", "No items selected to add!")
        return
    # --- Step 1: Retrieve what is already in today's menu ---
    existing_items_objs = retrieve_menu_by_date() # Returns list of full item dictionaries
    current_ids = []
    if existing_items_objs:
        # Extract just the ID strings from the existing objects
        for item in existing_items_objs:
            current_ids.append(str(item['id']))

    # Step 2: Merge new 'records' into current_ids 
    # We loop through new records and append them only if they aren't already there
    for new_id in records:
        if new_id not in current_ids:
            current_ids.append(new_id)

    # --- Step 3: Create the string and save ---
    ids_string = " ".join(current_ids)
    today_entry = {"date": date.today(), "item_ids": ids_string}
    
    # This overwrites the CSV entry for today, but now we are passing 
    # the COMBINED list of old + new items.
    add_entry_to_record(today_entry)
    update_today_view()
    # Clear selection after adding
    records.clear()
    messagebox.showinfo(
        "Success", "Items added to Today's menu successfully!"
    )


def on_add_item_popup():
    """Popup interface to add new item to Master Menu."""
    popup = tk.Toplevel(root)
    popup.title("Add New Item")
    popup.geometry("300x250")

    ttk.Label(popup, text="Item Name:").pack(pady=5)
    name_entry = ttk.Entry(popup)
    name_entry.pack(pady=5)

    ttk.Label(popup, text="Price:").pack(pady=5)
    price_entry = ttk.Entry(popup)
    price_entry.pack(pady=5)

    ttk.Label(popup, text="Category:").pack(pady=5)
    category_entry = ttk.Entry(popup)
    category_entry.pack(pady=5)

    def submit_item():
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        cat = category_entry.get().strip()

        if not name or not price or not cat:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Prepare dict for helper function
        new_record = {"item": name, "price": price, "category": cat}
        add_entry_to_master_menu(new_record)
        # Refresh Main Menu to show new item
        refresh_main_menu()
        popup.destroy()
        messagebox.showinfo("Success", f"{name} added to Master Menu.")

    ttk.Button(popup, text="Save Item", command=submit_item).pack(pady=10)


def get_price_filter():
    """Uses filter_numerical from data_handling2.py"""
    target_price = price_entry_hidden.get().strip()
    if not target_price:
        refresh_main_menu()  # Reset if empty
        return
    try:
        filtered_list = filter_numerical("price", target_price)

        # Clear existing items
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if filtered_list:
            for item in filtered_list:
                create_item_frame(scrollable_frame, item).pack(fill="x", pady=5)
        else:
            ttk.Label(
                scrollable_frame, text=f"No items found for price {target_price}"
            ).pack(pady=10)

    except ValueError:
        messagebox.showerror("Error", "Price must be a number")


def refresh_main_menu(custom_list=None):
    """
    Loads items into left scroll area.
    If custom_list is provided, it uses that. Otherwise, it fetches from master.
    """
    # Clear current widgets
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Decide which data to use
    if custom_list is not None:
        items_to_show = custom_list
    else:
        items_to_show = retrieve_master_menu()

    # Render items
    if items_to_show:
        for item in items_to_show:
            create_item_frame(scrollable_frame, item).pack(fill="x", pady=5)
    else:
        ttk.Label(scrollable_frame, text="No items found.").pack(pady=10)


def update_today_view():
    """Loads today's items into right scroll area."""
    for widget in right_scrollable_frame.winfo_children():
        widget.destroy()

    # Get items for today using helpers
    todays_items = retrieve_menu_by_date()  # defaults to today's date

    if todays_items:
        for item in todays_items:
            create_item_frame(right_scrollable_frame, item, show_checkbox=False).pack(
                fill="x", pady=5
            )
    else:
        ttk.Label(right_scrollable_frame, text="Menu not set for today.").pack(pady=10)


def on_option_select(event=None):
    """Handles Dropdown changes for Filtering and Sorting."""
    selected = selected_option.get()

    # --- UI Handling for "Enter Price" ---
    if selected == 'Price: "Enter price"':
        price_label.pack(side="left", padx=5)
        price_entry_hidden.pack(side="left", padx=5)
        apply_filter_btn.pack(side="left", padx=5)
        # We don't refresh here, we wait for the user to click "Apply"
    else:
        # Hide price inputs if they were visible
        price_label.pack_forget()
        price_entry_hidden.pack_forget()
        apply_filter_btn.pack_forget()

        # --- Sorting Logic ---
        all_items = retrieve_master_menu()

        if selected == "Price: Low to High":
            # Use the function from data_handling2
            sorted_list = sort_numerical(all_items, "price", "ascending")
            refresh_main_menu(sorted_list)

        elif selected == "Price: High to Low":
            # Use the function from data_handling2
            sorted_list = sort_numerical(all_items, "price", "descending")
            refresh_main_menu(sorted_list)

        elif selected == "Show All":
            refresh_main_menu()  # Reloads default order


# ... (Inside Main Window Setup) ...
# -------------------------
# Main Window Setup
# -------------------------
root = tk.Tk()
root.title("Canteen Inventory Manager")
root.geometry("1100x700")

# -- Outer Container --
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# -- Top Control Bar --
search_frame = ttk.Frame(main_frame)
search_frame.pack(fill="x", pady=5)

# Search
ttk.Label(search_frame, text="Search:").pack(side="left")
search_entry = ttk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)
ttk.Button(search_frame, text="Go", command=on_search).pack(side="left", padx=5)

# Buttons
ttk.Button(search_frame, text="Update Today's Menu", command=on_update).pack(
    side="left", padx=20
)
ttk.Button(search_frame, text="Add New Item", command=on_add_item_popup).pack(
    side="left", padx=5
)

# -- Filter section --
filter_frame = ttk.Frame(main_frame)
filter_frame.pack(fill="x", pady=5)

options = [
    "Show All",
    "Price: Low to High",
    "Price: High to Low",
    'Price: "Enter price"',
]

selected_option = tk.StringVar(value=options[0])
dropdown = ttk.Combobox(
    filter_frame,
    textvariable=selected_option,
    values=options,
    state="readonly",
    width=20,
)
dropdown.pack(side="left", padx=5)
dropdown.bind("<<ComboboxSelected>>", on_option_select)

# prices filter
price_label = ttk.Label(filter_frame, text="Price:")
price_entry_hidden = ttk.Entry(filter_frame, width=10)
apply_filter_btn = ttk.Button(filter_frame, text="Apply", command=get_price_filter)

# -------------------------
# Content Areas master_menu and todays_menu i.e left/right
# -------------------------
content_area = ttk.PanedWindow(main_frame, orient="horizontal")
content_area.pack(fill="both", expand=True, pady=10)

# --- LEFT: Master Menu ---
left_container = ttk.Frame(content_area, relief="sunken")
content_area.add(left_container, weight=3)

ttk.Label(left_container, text="Master Menu", font=("Arial", 14, "bold")).pack(pady=5)

canvas_l = tk.Canvas(left_container)
scroll_l = ttk.Scrollbar(left_container, orient="vertical", command=canvas_l.yview)
scrollable_frame = ttk.Frame(canvas_l)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas_l.configure(scrollregion=canvas_l.bbox("all"))
)
canvas_l.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_l.configure(yscrollcommand=scroll_l.set)

canvas_l.pack(side="left", fill="both", expand=True)
scroll_l.pack(side="right", fill="y")

# --- right: today's menu ---
right_container = ttk.Frame(content_area, relief="sunken")
content_area.add(right_container, weight=2)

ttk.Label(right_container, text="Today's Menu", font=("Arial", 14, "bold")).pack(pady=5)

canvas_r = tk.Canvas(right_container)
scroll_r = ttk.Scrollbar(right_container, orient="vertical", command=canvas_r.yview)
right_scrollable_frame = ttk.Frame(canvas_r)

right_scrollable_frame.bind(
    "<Configure>", lambda e: canvas_r.configure(scrollregion=canvas_r.bbox("all"))
)
canvas_r.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
canvas_r.configure(yscrollcommand=scroll_r.set)

canvas_r.pack(side="left", fill="both", expand=True)
scroll_r.pack(side="right", fill="y")


# --- scroll using scrollwheel ---
def _on_mousewheel(event):
    canvas_l.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas_r.yview_scroll(int(-1 * (event.delta / 120)), "units")


root.bind_all("<MouseWheel>", _on_mousewheel)

# -------------------------
# Initialization
# -------------------------
# Load initial data
refresh_main_menu()
update_today_view()

root.mainloop()
