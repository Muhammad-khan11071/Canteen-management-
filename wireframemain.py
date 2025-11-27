import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage
from PIL import Image, ImageTk
from data_manager import add_entry_to_master_menu as amm,retrieve_master_menu as rmm,add_entry_to_record,retrieve_record as retrive_today_record,retrieve_menu_by_date
from datetime import date
# from data_handling2 import filter_numerical as filter_price
records=[]
def add_ent(state,name,item_id):
    # record={"date":date.today(),"
    # item_ids":item_id}
    # add_entry_to_record(record)
    value=state.get()
    if value==1:
        if item_id not in records:
            records.append(str(item_id))
            print(records)
    else:
        if item_id in records:
            records.remove(item_id)
            print(records)


        


    
    
    
    # item_name = item_data['item']
    # is_available = item_data['is_available'].get() # Get the new state (True/False)
    
    # # item_data['frame'] is the reference to the actual ttk.Frame widget
    # parent_frame = item_data['frame'] 
    
    # print("-" * 40)
    # print(f"Checkbox for '{item_name}' was CLICKED.")
    # print(f"New state is: {is_available}")
    # print(f"Reference to the parent Frame widget: {parent_frame}")
    # print(f"Parent Frame ID: {parent_frame.winfo_id()}")
    # print("-" * 40)
    
    # # You can now manipulate the parent frame, e.g., change its border:
    # if is_available:
    #     parent_frame.config(relief="groove")
    # else:
    #     parent_frame.config(relief="solid")
# -------------------------
# Helper function to create an item card
# -------------------------
def create_item_frame(parent,record):
    item=record
    frame = ttk.Frame(parent, padding=10, relief="solid",width=500)
    frame.columnconfigure(0, weight=0)  # image column - fixed
    frame.columnconfigure(1, weight=0)  # spacer
    frame.columnconfigure(2, weight=1)  # info column - expands
    frame.columnconfigure(3, weight=0)  # delete button - fixed

    # Let the middle column expand

    # Image placeholder
    try:
        image = Image.open(rf"C:\Users\muhammad khan\OneDrive - Habib University\HU resources\Aps project\images\{item["id"]}.jpeg")
        image = image.resize((150, 100))  
        photo = ImageTk.PhotoImage(image)
    except FileNotFoundError:
        image = Image.open(rf"C:\Users\muhammad khan\OneDrive - Habib University\Desktop\Aps project\images\default.jpg")
        image = image.resize((150, 100))  
        photo = ImageTk.PhotoImage(image)
    

    img_label = ttk.Label(frame, image=photo, relief="ridge", width=30)
    if photo:
        img_label.config(image=photo)
        img_label.image = photo  # Prevent garbage collection
    else:
        img_label.config(text="[No Image Available]", anchor="center")
    img_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
    
 
    # Item info
    check_var=tk.IntVar()
    ttk.Label(frame, text=item["price"]).grid(row=0, column=2, sticky="w")
    ttk.Label(frame, text=item["item"]).grid(row=1, column=2, sticky="w")
    ttk.Label(frame, text="").grid(row=1, column=1, sticky="w")
    checkbox=tk.Checkbutton(frame,text="Available",variable=check_var,command=lambda state=check_var: add_ent(state,item["item"],item["id"])).grid(row=2,column=2,sticky="w")
    ttk.Label(frame, text=f"Category: {item["category"]}").grid(row=3, column=2, sticky="w")

    # ✅ Delete button (stick to east / right)
    delbt = tk.Button(
        frame,
        text="X",
        font=("Arial",10,"bold"),
        command=lambda: del_ent(frame, item["item"]),
        bg="red",
        fg="white",
        height=1, width=1,
    )
    delbt.grid(row=0, column=3, padx=10, sticky="e")
    # add_bt = tk.Button(
    #     frame,
    #     text="+",
    #     font=("Arial",15,"bold"),
    #     command=lambda: add_ent(frame, item["item"],item["id"]),
    #     bg="green",
    #     fg="white",
    #     height=1, width=1,
    # )
    # add_bt.grid(row=1, column=3, padx=10, sticky="e")
    # frame.pack_propagate(False)
    # lst.append(frame)

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
    record=""
    for i in records:
        record+=" "+str(i)
        print(record)
    today_date=date.today()
    dict={"date":today_date,"item_ids":record}
    add_entry_to_record(dict)
    update_today()


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
    category_entry = ttk.Entry(popup)
    category_entry.pack(pady=5)


    def add_item_to_main():
        """Add the new item to the main scrollable area."""
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        category = category_entry.get().strip()
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
        new_frame = create_item_frame(scrollable_frame, record)
        new_frame.pack(fill="x", pady=5)

        popup.destroy()  # close popup

    ttk.Button(popup, text="Add", command=add_item_to_main).pack(pady=10)
def on_option_select(event=None):
    selected = selected_option.get()

    if selected == 'Price: "Enter price"':
        price_entry_label.pack(pady=(5, 0), side="left")
        price_entry.pack(pady=(5, 0), side="left")
        apply_filter.pack(side="left", padx=5)

    # elif selected == "Price low to high":
    #     pass

    # else:
    #     price_entry_label.pack_forget()
    #     price_entry.pack_forget()

def retrive_from_main_menu():
    rm=rmm()
    for i in rm:
        new_frame = create_item_frame(scrollable_frame, i)
        new_frame.pack(fill="both",expand="True", pady=5,)
def update_today():
    for widget in right_scrollable_frame.winfo_children():
        widget.destroy()
    rm=retrieve_menu_by_date()
    for i in rm:
        print(i)
        new_frame = create_item_frame(right_scrollable_frame, i)
        new_frame.pack(fill="x", pady=5)
def add_to_todays_menu():
    rm=rmm()
    for i in rm:
        new_frame = create_item_frame(scrollable_frame, i)
        new_frame.pack(fill="x", pady=5)
def get_price():
    if not price_entry.get():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        rm=rmm()
        for i in rm:
            new_frame = create_item_frame(scrollable_frame, i)
            new_frame.pack(fill="x", pady=5)
        return

    item=rmm()
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    for i in item:
        print(price_entry.get())
        if int(i["price"])==int(price_entry.get()):
            new_frame = create_item_frame(scrollable_frame, i)
            
            new_frame.pack(fill="x", pady=5)





# -------------------------
# Main window setup
# -------------------------
root = tk.Tk()
root.title("Inventory Management GUI")
root.geometry("1100x700")

# Outer container frame
main_frame = ttk.Frame(root, padding=20, relief="solid")
main_frame.pack(fill="both", expand=True)

# Search + control buttons section
search_frame = ttk.Frame(main_frame)
search_frame.pack(fill="both", pady=5)

search_entry = ttk.Entry(search_frame, width=50)
search_entry.pack(side="left", padx=5)

search_button = ttk.Button(search_frame, text="Search", command=on_search)
search_button.pack(side="left", padx=5)

update_button = ttk.Button(search_frame, text="Update", command=on_update)
update_button.pack(side="left", padx=5)

# ✅ This is the permanent "Add Item" button in the main window2
add_button = ttk.Button(search_frame, text="Add Item", command=on_add_item_popup)
add_button.pack(side="left", padx=5)
from tkinter import ttk

# --- define the function that handles dropdown selection ---

# --- dropdown setup ---
options = [
    "Price high to low",
    "Price low to high",
    'Price: "Enter price"'
]

selected_option = tk.StringVar(value=options[0])

dropdown = ttk.Combobox(search_frame, textvariable=selected_option, values=options, state="readonly")
dropdown.pack(pady=10,side="left")   # you can replace with .grid() or .place() if you’re using those
dropdown.bind("<<ComboboxSelected>>", on_option_select)

# --- entry (hidden by default) ---
price_entry_label = ttk.Label(search_frame, text="Enter custom price:")
price_entry = ttk.Entry(search_frame)
apply_filter = ttk.Button(search_frame, text="Applly", command=get_price)



# Scrollable items area
items_frame_container = ttk.Frame(main_frame,width=500)
items_frame_container.pack(fill="both", expand=True, pady=10,side="left")

canvas = tk.Canvas(items_frame_container,width=500)
scrollbar = ttk.Scrollbar(items_frame_container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas,width=500)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="y", expand=False)
scrollbar.pack(side="left", fill="both")
# --- ADD THIS NEW CODE FOR THE RIGHT MENU ---
right_menu_container = ttk.Frame(main_frame, padding=10, relief="solid")
right_menu_container.pack(fill="y", expand=False, side="left", padx=(10, 0))

# 2. Create the Canvas and Scrollbar INSIDE this container
right_canvas = tk.Canvas(right_menu_container)
right_scrollbar = ttk.Scrollbar(right_menu_container, orient="vertical", command=right_canvas.yview)

# 3. Create the frame that will hold the content
right_scrollable_frame = ttk.Frame(right_canvas)

# 4. Wire them all together
right_scrollable_frame.bind(
    "<Configure>",
    lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
)

right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
right_canvas.configure(yscrollcommand=right_scrollbar.set)

# 5. Pack the canvas and scrollbar (note 'side="right"' for the scrollbar)
right_canvas.pack(side="left", fill="y", expand=False)
right_scrollbar.pack(side="right", fill="y",expand=False)

# 6. Add placeholder content to the *new scrollable frame*
ttk.Label(right_scrollable_frame, text="Todays menu ", font=("Arial", 16, "bold")).pack(pady=10)
ttk.Label(right_scrollable_frame, text="There is nothing to show here right now.").pack(pady=5)

# Add a bunch of labels to prove scrolling works


# --- END OF NEW CODE ---

def _on_mousewheel(event):
    # Find the widget under the cursor
    x, y = event.x_root, event.y_root
    widget = root.winfo_containing(x, y) # 'root' is your main window

    # Check if the widget is the left canvas or one of its children
    # We do this by checking if the widget's string "path" starts with the canvas's path
    if str(widget).startswith(str(canvas)):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    # Check if the widget is the right canvas or one of its children
    elif str(widget).startswith(str(right_canvas)):
        right_canvas.yview_scroll(-1 * (event.delta // 120), "units")

def _on_mousewheel_linux(event):
    # Find the widget under the cursor
    x, y = event.x_root, event.y_root
    widget = root.winfo_containing(x, y) 

    target_canvas = None
    
    # Check if the widget is the left canvas or one of its children
    if str(widget).startswith(str(canvas)):
        target_canvas = canvas
    # Check if the widget is the right canvas or one of its children
    elif str(widget).startswith(str(right_canvas)):
        target_canvas = right_canvas
    
    if target_canvas:
        # Scroll the correct canvas (Linux)
        if event.num == 4:
            target_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            target_canvas.yview_scroll(1, "units")

# Bind both types
canvas.bind_all("<MouseWheel>", _on_mousewheel)        # Windows / Mac
# canvas.bind_all("<Button-4>", _on_mousewheel_linux)    # Linux scroll up
# canvas.bind_all("<Button-5>", _on_mousewheel_linux) 


     # Windows / Mac
# canvas.bind_all("<Button-4>", _on_mousewheel_linux)    # Linux scroll up
# canvas.bind_all("<Button-5>", _on_mousewheel_linux) 

# Add a few sample items
retrive_from_main_menu()


root.mainloop()
