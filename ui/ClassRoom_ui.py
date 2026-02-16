import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from models.ClassRoom import ClassRoom


# ================= ADD =================
def add_classroom():
    win = tk.Toplevel()
    win.title("Add Class Room")
    win.geometry("400x420")
    win.grab_set()

    tk.Label(win, text="Add Class Room", font=("Arial", 16)).pack(pady=10)

    tk.Label(win, text="Class Name").pack()
    entry_name = tk.Entry(win)
    entry_name.pack()

    tk.Label(win, text="Class Grade").pack()
    grade_var = tk.StringVar()
    combo_grade = ttk.Combobox(
        win, textvariable=grade_var,
        values=["7", "8", "9"], state="readonly"
    )
    combo_grade.pack()
    combo_grade.current(0)

    tk.Label(win, text="Capacity (1–30)").pack()
    entry_capacity = tk.Entry(win)
    entry_capacity.pack()

    def save():
        try:
            ClassRoom(
                class_name=entry_name.get(),
                class_grade=int(grade_var.get()),
                capacity=int(entry_capacity.get())
            )
            messagebox.showinfo("Success", "Class Room added successfully", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    tk.Button(win, text="Save", width=25, command=save).pack(pady=10)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= SHOW ALL =================
def show_all_classrooms():
    win = tk.Toplevel()
    win.title("All Class Rooms")
    win.geometry("600x400")
    win.grab_set()

    tk.Label(win, text="All Class Rooms", font=("Arial", 16)).pack(pady=10)

    listbox = tk.Listbox(win, width=100)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    for info in ClassRoom.show_all():
        listbox.insert(tk.END, info)

    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=10)


# ================= SEARCH =================
def search_classroom():
    win = tk.Toplevel()
    win.title("Search Class Room")
    win.geometry("400x300")
    win.grab_set()

    tk.Label(win, text="Search Class Room", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Class ID").pack()

    entry_id = tk.Entry(win)
    entry_id.pack()

    result = tk.Label(win, text="", justify="left")
    result.pack(pady=10)

    def search():
        try:
            cid = int(entry_id.get())
            classroom = ClassRoom.search_by_id(cid)
            if classroom is None:
                messagebox.showerror("Error", "Class Room not found", parent=win)
                result.config(text="")
            else:
                result.config(
                    text=
                    f"ID: {classroom.class_id}\n"
                    f"Name: {classroom.class_name}\n"
                    f"Grade: {classroom.class_grade}\n"
                    f"Capacity: {classroom.capacity}"
                )
        except ValueError:
            messagebox.showerror("Error", "Invalid ID", parent=win)

    tk.Button(win, text="Search", width=25, command=search).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= REMOVE =================
def remove_classroom():
    win = tk.Toplevel()
    win.title("Remove Class Room")
    win.geometry("400x250")
    win.grab_set()

    tk.Label(win, text="Remove Class Room", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Class ID").pack()

    entry_id = tk.Entry(win)
    entry_id.pack()

    def remove():
        try:
            cid = int(entry_id.get())
            classroom = ClassRoom.search_by_id(cid)
            if classroom:
                classroom.remove()
                messagebox.showinfo("Success", "Class Room removed", parent=win)
                win.destroy()
            else:
                messagebox.showerror("Error", "Class Room not found", parent=win)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID", parent=win)

    tk.Button(win, text="Remove", width=25, command=remove).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= EDIT =================
def edit_classroom():
    win = tk.Toplevel()
    win.title("Edit Class Room")
    win.geometry("400x300")
    win.grab_set()

    tk.Label(win, text="Edit Class Room", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Class ID").pack()

    entry_id = tk.Entry(win)
    entry_id.pack()

    def search_and_edit():
        try:
            cid = int(entry_id.get())
            classroom = ClassRoom.search_by_id(cid)
            if classroom is None:
                messagebox.showerror("Error", "Class Room not found", parent=win)
                return

            if hasattr(win, "form"):
                win.form.destroy()

            win.geometry("400x520")
            win.form = tk.Frame(win)
            win.form.pack(pady=10)

            tk.Label(win.form, text="Class Name").pack()
            entry_name = tk.Entry(win.form)
            entry_name.pack()
            entry_name.insert(0, classroom.class_name)

            tk.Label(win.form, text="Class Grade").pack()
            grade_var = tk.StringVar(value=str(classroom.class_grade))
            combo_grade = ttk.Combobox(
                win.form, textvariable=grade_var,
                values=["7", "8", "9"], state="readonly"
            )
            combo_grade.pack()

            tk.Label(win.form, text="Capacity").pack()
            entry_capacity = tk.Entry(win.form)
            entry_capacity.pack()
            entry_capacity.insert(0, str(classroom.capacity))

            def save_edit():
                try:
                    classroom.edit(
                        class_name=entry_name.get(),
                        n_class_grade=int(grade_var.get()),
                        n_capacity=int(entry_capacity.get())
                    )
                    messagebox.showinfo("Success", "Class Room updated successfully", parent=win)
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=win)

            tk.Button(win.form, text="Save Changes", width=25, command=save_edit).pack(pady=10)

        except ValueError:
            messagebox.showerror("Error", "ID must be a number", parent=win)

    tk.Button(win, text="Search", width=25, command=search_and_edit).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=10)
