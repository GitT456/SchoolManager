import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from models.member import Member

# ================= ADD =================
def add_member(root=None):
    win = tk.Toplevel(root)
    win.title("Add Member")
    win.geometry("420x650")
    win.grab_set()

    tk.Label(win, text="Add New Member", font=("Arial", 16)).pack(pady=10)
    form = tk.Frame(win)
    form.pack(pady=10)

    def field(label):
        tk.Label(form, text=label).pack()
        e = tk.Entry(form)
        e.pack()
        return e

    entry_name = field("Name")
    entry_lname = field("Last Name")
    entry_ncode = field("National Code")
    entry_age = field("Age")
    entry_phone = field("Phone")
    entry_address = field("Address")
    entry_membership = field("Membership Number")
    entry_username = field("Username")
    entry_password = field("Password")

    def save_member():
        try:
            Member(
                name=entry_name.get(),
                lname=entry_lname.get(),
                ncode=entry_ncode.get(),
                age=int(entry_age.get()),
                phone=entry_phone.get(),
                address=entry_address.get(),
                membership_num=entry_membership.get(),
                username=entry_username.get(),
                password=entry_password.get()
            )
            messagebox.showinfo("Success", "Member added successfully", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    tk.Button(win, text="Save Member", width=25, command=save_member).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= SHOW ALL =================
def show_all_members(root=None):
    win = tk.Toplevel(root)
    win.title("All Members")
    win.geometry("700x400")
    win.grab_set()

    tk.Label(win, text="All Members", font=("Arial", 16)).pack(pady=10)

    listbox = tk.Listbox(win, width=120)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    for m in Member.show_all():
        listbox.insert(tk.END, m)

    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=10)


# ================= SEARCH =================
def search_member(root=None):
    win = tk.Toplevel(root)
    win.title("Search Member")
    win.geometry("400x400")
    win.grab_set()

    tk.Label(win, text="Search Member", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Membership Number").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    result = tk.Label(win, text="", justify="left")
    result.pack(pady=10)

    def search():
        member = Member.search_by_membership_num(entry_id.get())
        if member is None:
            messagebox.showerror("Error", "Member not found", parent=win)
            result.config(text="")
        else:
            result.config(
                text=(
                    f"Name: {member.name}\n"
                    f"Last Name: {member.lname}\n"
                    f"National Code: {member.ncode}\n"
                    f"Age: {member.age}\n"
                    f"Phone: {member.phone}\n"
                    f"Address: {member.address}\n"
                    f"Membership: {member.membership_num}\n"
                    f"Username: {member.username}\n"
                    f"Password: {member.password}"
                )
            )

    tk.Button(win, text="Search", width=25, command=search).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= REMOVE =================
def remove_member(root=None):
    win = tk.Toplevel(root)
    win.title("Remove Member")
    win.geometry("400x250")
    win.grab_set()

    tk.Label(win, text="Remove Member", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Membership Number").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    def remove():
        member = Member.search_by_membership_num(entry_id.get())
        if member is None:
            messagebox.showerror("Error", "Member not found", parent=win)
        else:
            member.remove()
            messagebox.showinfo("Success", "Member removed", parent=win)
            win.destroy()

    tk.Button(win, text="Remove", width=25, command=remove).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)


# ================= EDIT =================
def edit_member(root=None):
    win = tk.Toplevel(root)
    win.title("Edit Member")
    win.geometry("400x750")
    win.grab_set()

    tk.Label(win, text="Edit Member", font=("Arial", 16)).pack(pady=10)
    tk.Label(win, text="Membership Number").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    def search_and_edit():
        # پاک کردن فرم قبلی
        if hasattr(win, "form"):
            win.form.destroy()

        member = Member.search_by_membership_num(entry_id.get())
        if member is None:
            messagebox.showerror("Error", "Member not found", parent=win)
            return

        win.geometry("400x750")
        win.form = tk.Frame(win)
        win.form.pack(pady=10)

        def field(label, value=""):
            tk.Label(win.form, text=label).pack()
            e = tk.Entry(win.form)
            e.pack()
            e.insert(0, value)
            return e

        entry_name = field("Name", member.name)
        entry_lname = field("Last Name", member.lname)
        entry_ncode = field("National Code", member.ncode)
        entry_age = field("Age", member.age)
        entry_phone = field("Phone", member.phone)
        entry_address = field("Address", member.address)
        entry_membership = field("Membership Number", member.membership_num)
        entry_username = field("Username", member.username)
        entry_password = field("Password", member.password)

        def save_edit():
            try:
                member.edit(
                    n_name=entry_name.get(),
                    n_lname=entry_lname.get(),
                    n_ncode=entry_ncode.get(),
                    n_age=int(entry_age.get()),
                    n_phone=entry_phone.get(),
                    n_address=entry_address.get(),
                    n_membership_num=entry_membership.get(),
                    n_username=entry_username.get(),
                    n_password=entry_password.get()
                )
                messagebox.showinfo("Success", "Member edited successfully", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        tk.Button(win.form, text="Save Changes", width=25, command=save_edit).pack(pady=5)

    tk.Button(win, text="Search", width=25, command=search_and_edit).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)
