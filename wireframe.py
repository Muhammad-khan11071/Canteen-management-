import tkinter as tk
from tkinter import ttk, messagebox
from datamanager import add_entry_to_master_menu as amm,retrieve_master_menu as rmm

# -------------------------
# Helper function to create an item card
# -------------------------
def create_item_frame(parent, item_name="Item name", price="Price", available="0"):
    frame = ttk.Frame(parent, padding=10, relief="solid")

    # Let the middle column expand
    frame.columnconfigure(1, weight=1)

    # Image placeholder
    img_frame = ttk.Label(frame, text="[Image]", relief="ridge", width=20, anchor="center")
    img_frame.grid(row=0, column=0, rowspan=3, padx=5, pady=5)

    # Item info
    ttk.Label(frame, text=price).grid(row=0, column=1, sticky="w")
    ttk.Label(frame, text=item_name).grid(row=1, column=1, sticky="w")
    ttk.Label(frame, text=f"Category: {available}").grid(row=2, column=1, sticky="w")

    # ✅ Delete button (stick to east / right)
    delbt = tk.Button(
        frame,
        text="Delete",
        command=lambda: del_ent(frame, item_name),
        bg="red",
        fg="white"
    )
    delbt.grid(row=0, column=2, rowspan=3, padx=10, sticky="e")

    return frame
# -------------------------
# Button callbacks
# -------------------------
def del_ent(frame,name):
    if messagebox.askyesno("Delete Item", f"Are you sure you want to delete '{name}'?"):
        frame.destroy()
        print(f"Deleted: {name}")
def on_search():
    query = search_entry.get()
    print(f"Searching for: {query}")


def on_update():
    print("Update button clicked!")


def on_add_item_popup():
    """Open a popup to add a new item."""
    popup = tk.Toplevel(root)
    popup.title("Add New Item")
    popup.geometry("300x250")
    popup.resizable(False, False)

    ttk.Label(popup, text="Item Name:").pack(pady=5)
    name_entry = ttk.Entry(popup)
    name_entry.pack(pady=5)

    ttk.Label(popup, text="Price:").pack(pady=5)
    price_entry = ttk.Entry(popup)
    price_entry.pack(pady=5)

    ttk.Label(popup, text="Category:").pack(pady=5)
    avail_entry = ttk.Entry(popup)
    avail_entry.pack(pady=5)

    def add_item_to_main():
        """Add the new item to the main scrollable area."""
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        category = avail_entry.get().strip()
        record={
            'item': name,
            'price': price,
            'category': category
        }
        amm(record)
        if not name or not price or not category:
            messagebox.showwarning("Missing Info", "Please fill all fields!")
            return
        # Create and pack new item in the main list
        new_frame = create_item_frame(scrollable_frame, name, f"Price: ${price}", category)
        new_frame.pack(fill="x", pady=5)

        popup.destroy()  # close popup

    ttk.Button(popup, text="Add", command=add_item_to_main).pack(pady=10)
def retrive_from_main_menu():
    rm=rmm()
    for i in rm:
        new_frame = create_item_frame(scrollable_frame, i["item"], f"Price: ${i["price"]}", i["category"])
        new_frame.pack(fill="x", pady=5)


# -------------------------
# Main window setup
# -------------------------
root = tk.Tk()
root.title("Inventory Management GUI")
root.geometry("800x500")

# Outer container frame
main_frame = ttk.Frame(root, padding=20, relief="solid")
main_frame.pack(fill="both", expand=True)

# Search + control buttons section
search_frame = ttk.Frame(main_frame)
search_frame.pack(fill="x", pady=5)

search_entry = ttk.Entry(search_frame, width=50)
search_entry.pack(side="left", padx=5)

search_button = ttk.Button(search_frame, text="Search", command=on_search)
search_button.pack(side="left", padx=5)

update_button = ttk.Button(search_frame, text="Update", command=on_update)
update_button.pack(side="left", padx=5)

# ✅ This is the permanent "Add Item" button in the main window
add_button = ttk.Button(search_frame, text="Add Item", command=on_add_item_popup)
add_button.pack(side="left", padx=5)

# Scrollable items area
items_frame_container = ttk.Frame(main_frame)
items_frame_container.pack(fill="both", expand=True, pady=10)

canvas = tk.Canvas(items_frame_container)
scrollbar = ttk.Scrollbar(items_frame_container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
def _on_mousewheel(event):
    # For Windows and Mac
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def _on_mousewheel_linux(event):
    # For Linux (uses Button-4 / Button-5)
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")

# Bind both types
canvas.bind_all("<MouseWheel>", _on_mousewheel)        # Windows / Mac
canvas.bind_all("<Button-4>", _on_mousewheel_linux)    # Linux scroll up
canvas.bind_all("<Button-5>", _on_mousewheel_linux) 

# Add a few sample items
retrive_from_main_menu()


root.mainloop()
