import tkinter as tk
from tkinter import ttk, messagebox
from models.lib_item import Item, Book, Magazine, DVD

CATEGORY_OPTIONS = ["Fantasy", "Science", "Movie", "History", "Technology", "Art"]

# -------------------------- Add Item --------------------------
def add_item(root=None):
    win = tk.Toplevel(root)
    win.title("Add Library Item")
    win.geometry("500x700")
    win.grab_set()

    tk.Label(win, text="Add New Item", font=("Arial", 16)).pack(pady=10)

    tk.Label(win, text="Select Item Type").pack()
    item_type_var = tk.StringVar(value="Book")
    combo_type = ttk.Combobox(win, textvariable=item_type_var, values=["Book", "Magazine", "DVD"], state="readonly")
    combo_type.pack(pady=5)

    form_frame = tk.Frame(win)
    form_frame.pack(pady=10)
    fields = {}
    category_var = tk.StringVar(value=CATEGORY_OPTIONS[0])

    def build_form(item_type):
        for widget in form_frame.winfo_children():
            widget.destroy()
        fields.clear()

        
        for label_text in ["Name", "Price", "Category", "Year"]:
            tk.Label(form_frame, text=label_text).pack()
            if label_text == "Category":
                entry = ttk.Combobox(form_frame, values=CATEGORY_OPTIONS, state="readonly", textvariable=category_var)
            else:
                entry = tk.Entry(form_frame)
            entry.pack()
            fields[label_text] = entry

        
        if item_type == "Book":
            for label_text in ["Author", "ISBN", "Num Page"]:
                tk.Label(form_frame, text=label_text).pack()
                entry = tk.Entry(form_frame)
                entry.pack()
                fields[label_text] = entry
        elif item_type == "Magazine":
            tk.Label(form_frame, text="Num Page").pack()
            entry = tk.Entry(form_frame)
            entry.pack()
            fields["Num Page"] = entry
        elif item_type == "DVD":
            for label_text in ["Duration", "Num File"]:
                tk.Label(form_frame, text=label_text).pack()
                entry = tk.Entry(form_frame)
                entry.pack()
                fields[label_text] = entry

    build_form(item_type_var.get())
    combo_type.bind("<<ComboboxSelected>>", lambda e: build_form(item_type_var.get()))

    def save_item():
        item_type = item_type_var.get()
        try:
            common_args = {
                "name": fields["Name"].get(),
                "price": float(fields["Price"].get()),
                "category": category_var.get(),
                "year": int(fields["Year"].get())
            }

            if item_type == "Book":
                item = Book(**common_args,
                            author=fields["Author"].get(),
                            isbn=fields["ISBN"].get(),
                            num_page=int(fields["Num Page"].get()))
                item.add()  
            elif item_type == "Magazine":
                item = Magazine(**common_args,
                                num_page=int(fields["Num Page"].get()))
                item.add()
            elif item_type == "DVD":
                item = DVD(**common_args,
                           duration=int(fields["Duration"].get()),
                           num_file=int(fields["Num File"].get()))
                item.add()

            messagebox.showinfo("Success", f"{item_type} added successfully")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Save Item", width=25, command=save_item).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# -------------------------- Edit Item --------------------------
def edit_item(root=None):
    win = tk.Toplevel(root)
    win.title("Edit Item")
    win.geometry("500x700")
    win.grab_set()

    tk.Label(win, text="Edit Item", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Item ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    form_frame = tk.Frame(win)
    form_frame.pack(pady=10)
    fields = {}
    category_var = tk.StringVar()

    def search_and_edit():
        try:
            item_id = int(entry_id.get())
            item = Item.search_by_id(item_id)
            if not item:
                messagebox.showerror("Error", f"Item with ID {item_id} not found")
                return
                
            for widget in form_frame.winfo_children():
                widget.destroy()
            fields.clear()

            
            category_var.set(getattr(item, "category", CATEGORY_OPTIONS[0]))
            for label_text in ["Name", "Price", "Category", "Year"]:
                tk.Label(form_frame, text=label_text).pack()
                if label_text == "Category":
                    entry = ttk.Combobox(form_frame, values=CATEGORY_OPTIONS, state="readonly", textvariable=category_var)
                else:
                    entry = tk.Entry(form_frame)
                    entry.insert(0, str(getattr(item, label_text.lower(), "")))
                entry.pack()
                fields[label_text] = entry

            
            if isinstance(item, Book):
                for label_text, attr in [("Author", "author"), ("ISBN", "isbn"), ("Num Page", "num_page")]:
                    tk.Label(form_frame, text=label_text).pack()
                    entry = tk.Entry(form_frame)
                    entry.insert(0, str(getattr(item, attr, "")))
                    entry.pack()
                    fields[label_text] = entry
            elif isinstance(item, Magazine):
                tk.Label(form_frame, text="Num Page").pack()
                entry = tk.Entry(form_frame)
                entry.insert(0, str(item.num_page))
                entry.pack()
                fields["Num Page"] = entry
            elif isinstance(item, DVD):
                for label_text, attr in [("Duration", "duration"), ("Num File", "num_file")]:
                    tk.Label(form_frame, text=label_text).pack()
                    entry = tk.Entry(form_frame)
                    entry.insert(0, str(getattr(item, attr, "")))
                    entry.pack()
                    fields[label_text] = entry

        
            def do_edit():
                try:
                    
                    common_args = {
                        "n_name": fields["Name"].get(),
                        "n_price": float(fields["Price"].get()),
                        "n_category": category_var.get(), 
                        "n_year": int(fields["Year"].get())
                    }

                    if isinstance(item, Book):
                        item.edit(**common_args,
                                  n_author=fields["Author"].get(),
                                  n_isbn=fields["ISBN"].get(),
                                  n_page_num=int(fields["Num Page"].get()))
                    elif isinstance(item, Magazine):
                        item.edit(**common_args,
                                  n_page_num=int(fields["Num Page"].get()))
                    elif isinstance(item, DVD):
                        item.edit(**common_args,
                                  n_duration=int(fields["Duration"].get()),
                                  n_num_file=int(fields["Num File"].get()))

                    messagebox.showinfo("Success", f"Item (ID: {item.id}) edited successfully")
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(form_frame, text="Save Edit", width=25, command=do_edit).pack(pady=5)

        except ValueError:
            messagebox.showerror("Error", "Item ID must be a number")

    tk.Button(win, text="Search", width=25, command=search_and_edit).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# -------------------------- Remove Item --------------------------
def remove_item(root=None):
    win = tk.Toplevel(root)
    win.title("Remove Item")
    win.geometry("400x250")
    win.grab_set()

    tk.Label(win, text="Remove Item", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Item ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    def do_remove():
        try:
            item_id = int(entry_id.get())
            item = Item.search_by_id(item_id)
            if not item:
                messagebox.showerror("Error", f"Item with ID {item_id} not found")
                return
            item.remove()
            messagebox.showinfo("Success", "Item removed successfully")
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Item ID must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Remove", width=25, command=do_remove).pack(pady=10)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# -------------------------- Show All Items --------------------------
def show_all_items(root=None):
    win = tk.Toplevel(root)
    win.title("All Items")
    win.geometry("700x400")

    tk.Label(win, text="All Library Items", font=("Arial", 16)).pack(pady=10)
    listbox = tk.Listbox(win, width=120)
    listbox.pack(padx=10, pady=10, fill="both", expand=True)

    all_items_info = Item.show_all()
    for info in all_items_info:
        listbox.insert(tk.END, info)

    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=10)


# -------------------------- Search Item --------------------------
def search_item(root=None):
    win = tk.Toplevel(root)
    win.title("Search Item")
    win.geometry("500x500")
    win.grab_set()

    tk.Label(win, text="Search Item", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Item ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    result_label = tk.Label(win, text="", justify="left")
    result_label.pack(pady=10)

    def do_search():
        try:
            item_id = int(entry_id.get())
            item = Item.search_by_id(item_id)
            if not item:
                result_label.config(text="")
                messagebox.showerror("Error", f"Item with ID {item_id} not found")
                return
            info = f"ID: {item.id}\nName: {item.name}\nCategory: {item.category}\nPrice: {item.price}\nYear: {item.year}\n"
            if isinstance(item, Book):
                info += f"Author: {item.author}\nISBN: {item.isbn}\nNum Page: {item.num_page}"
            elif isinstance(item, Magazine):
                info += f"Num Page: {item.num_page}"
            elif isinstance(item, DVD):
                info += f"Duration: {item.duration}\nNum File: {item.num_file}"
            result_label.config(text=info)
        except ValueError:
            messagebox.showerror("Error", "Item ID must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Search", width=25, command=do_search).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)
