import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from models.Subject import Subject


# ================= ADD =================
def add_subject():
    win = tk.Toplevel()
    win.title("Add Subject")
    win.geometry("400x420")
    win.grab_set()

    tk.Label(win, text="Add Subject", font=("Arial", 16)).pack(pady=10)

    tk.Label(win, text="Subject Name").pack()
    entry_name = tk.Entry(win)
    entry_name.pack()

    tk.Label(win, text="Teacher").pack()
    entry_teacher = tk.Entry(win)
    entry_teacher.pack()

    tk.Label(win, text="Grade").pack()
    grade_var = tk.StringVar()
    combo_grade = ttk.Combobox(
        win, textvariable=grade_var,
        values=["7", "8", "9"], state="readonly"
    )
    combo_grade.pack()
    combo_grade.current(0)

    tk.Label(win, text="Category").pack()
    entry_category = tk.Entry(win)
    entry_category.pack()

    def save():
        try:
            Subject(
                subject_name=entry_name.get(),
                subject_teacher=entry_teacher.get(),
                subject_grade=int(grade_var.get()),
                subject_category=entry_category.get()
            )
            messagebox.showinfo("Success", "Subject added successfully", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    tk.Button(win, text="Save", width=25, command=save).pack(pady=10)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= SHOW ALL =================
def show_all_subjects():
    win = tk.Toplevel()
    win.title("All Subjects")
    win.geometry("600x400")
    win.grab_set()

    tk.Label(win, text="All Subjects", font=("Arial", 16)).pack(pady=10)

    listbox = tk.Listbox(win, width=100)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    for info in Subject.show_all():
        listbox.insert(tk.END, info)

    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=10)


# ================= SEARCH =================
def search_subject():
    win = tk.Toplevel()
    win.title("Search Subject")
    win.geometry("400x300")
    win.grab_set()

    tk.Label(win, text="Search Subject", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Subject ID").pack()

    entry_id = tk.Entry(win)
    entry_id.pack()

    result = tk.Label(win, text="", justify="left")
    result.pack(pady=10)

    def search():
        try:
            sid = int(entry_id.get())
            subject = Subject.search_by_id(sid)
            if subject is None:
                messagebox.showerror("Error", "Subject not found", parent=win)
                result.config(text="")
            else:
                result.config(
                    text=
                    f"ID: {subject.subject_id}\n"
                    f"Name: {subject.subject_name}\n"
                    f"Teacher: {subject.subject_teacher}\n"
                    f"Grade: {subject.subject_grade}\n"
                    f"Category: {subject.subject_category}"
                )
        except ValueError:
            messagebox.showerror("Error", "Invalid ID", parent=win)

    tk.Button(win, text="Search", width=25, command=search).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= REMOVE =================
def remove_subject():
    win = tk.Toplevel()
    win.title("Remove Subject")
    win.geometry("400x250")
    win.grab_set()

    tk.Label(win, text="Remove Subject", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Subject ID").pack()

    entry_id = tk.Entry(win)
    entry_id.pack()

    def remove():
        try:
            sid = int(entry_id.get())
            subject = Subject.search_by_id(sid)
            if subject:
                subject.remove()
                messagebox.showinfo("Success", "Subject removed successfully", parent=win)
                win.destroy()
            else:
                messagebox.showerror("Error", "Subject not found", parent=win)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID", parent=win)

    tk.Button(win, text="Remove", width=25, command=remove).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= EDIT =================
def edit_subject():
    win = tk.Toplevel()
    win.title("Edit Subject")
    win.geometry("400x300")
    win.grab_set()

    tk.Label(win, text="Edit Subject", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Subject ID").pack()

    entry_id = tk.Entry(win)
    entry_id.pack()

    def search_and_edit():
        try:
            sid = int(entry_id.get())
            subject = Subject.search_by_id(sid)
            if subject is None:
                messagebox.showerror("Error", "Subject not found", parent=win)
                return

            if hasattr(win, "form"):
                win.form.destroy()

            win.geometry("400x520")
            win.form = tk.Frame(win)
            win.form.pack(pady=10)

            tk.Label(win.form, text="Subject Name").pack()
            entry_name = tk.Entry(win.form)
            entry_name.pack()
            entry_name.insert(0, subject.subject_name)

            tk.Label(win.form, text="Teacher").pack()
            entry_teacher = tk.Entry(win.form)
            entry_teacher.pack()
            entry_teacher.insert(0, subject.subject_teacher)

            tk.Label(win.form, text="Grade").pack()
            grade_var = tk.StringVar(value=str(subject.subject_grade))
            combo_grade = ttk.Combobox(
                win.form, textvariable=grade_var,
                values=["7", "8", "9"], state="readonly"
            )
            combo_grade.pack()

            tk.Label(win.form, text="Category").pack()
            entry_category = tk.Entry(win.form)
            entry_category.pack()
            entry_category.insert(0, subject.subject_category)

            def save_edit():
                try:
                    subject.edit(
                        n_subject_name=entry_name.get(),
                        n_subject_teacher=entry_teacher.get(),
                        n_subject_grade=int(grade_var.get()),
                        n_subject_category=entry_category.get()
                    )
                    messagebox.showinfo("Success", "Subject updated successfully", parent=win)
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=win)

            tk.Button(win.form, text="Save Changes", width=25, command=save_edit).pack(pady=10)

        except ValueError:
            messagebox.showerror("Error", "ID must be a number", parent=win)

    tk.Button(win, text="Search", width=25, command=search_and_edit).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=10)
