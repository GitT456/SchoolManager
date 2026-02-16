import tkinter as tk
from tkinter import ttk, messagebox
from models.SchoolEmployee import *

SHIFT_OPTIONS = ["Morning", "Afternoon", "Evening"]
EDU_OPTIONS = ["High School", "Bachelor", "Master", "PhD"]
EMP_TYPES = ["SchoolManager", "AssistantPrincipal", "Teacher", "Janitor"]


# ========================== ADD ==========================
def add_employee(root=None):
    win = tk.Toplevel(root)
    win.title("Add Employee")
    win.geometry("500x800")
    win.grab_set()

    tk.Label(win, text="Add New Employee", font=("Arial", 16)).pack(pady=10)

    tk.Label(win, text="Select Employee Type").pack()
    emp_type_var = tk.StringVar(value="Teacher")
    combo_type = ttk.Combobox(win, values=EMP_TYPES,
                              textvariable=emp_type_var, state="readonly")
    combo_type.pack(pady=5)

    form_frame = tk.Frame(win)
    form_frame.pack(pady=10)
    fields = {}

    def build_form(emp_type):
        for w in form_frame.winfo_children():
            w.destroy()
        fields.clear()

        # -------- common fields --------
        for label in ["Name", "Last Name", "National Code", "Age",
                      "Phone", "Address", "Salary", "Shift",
                      "Education Level", "Major", "Work Experience"]:

            tk.Label(form_frame, text=label).pack()

            if label == "Shift":
                entry = ttk.Combobox(form_frame, values=SHIFT_OPTIONS, state="readonly")
                entry.current(0)
            elif label == "Education Level":
                entry = ttk.Combobox(form_frame, values=EDU_OPTIONS, state="readonly")
                entry.current(0)
            else:
                entry = tk.Entry(form_frame)

            entry.pack()
            fields[label] = entry

        # -------- specific fields --------
        if emp_type == "SchoolManager":
            for l in ["License Number", "Room Number"]:
                tk.Label(form_frame, text=l).pack()
                e = tk.Entry(form_frame)
                e.pack()
                fields[l] = e

        elif emp_type == "AssistantPrincipal":
            for l in ["Department", "Teaching Hours"]:
                tk.Label(form_frame, text=l).pack()
                e = tk.Entry(form_frame)
                e.pack()
                fields[l] = e

        elif emp_type == "Teacher":
            for l in ["Subject Name", "Teaching Hours",
                      "Teaching Days", "Overtime Hours"]:
                tk.Label(form_frame, text=l).pack()
                e = tk.Entry(form_frame)
                e.pack()
                fields[l] = e

        elif emp_type == "Janitor":
            tk.Label(form_frame, text="Duties").pack()
            e = tk.Entry(form_frame)
            e.pack()
            fields["Duties"] = e

    build_form(emp_type_var.get())
    combo_type.bind("<<ComboboxSelected>>",
                    lambda e: build_form(emp_type_var.get()))

    def save_employee():
        try:
            common = dict(
                name=fields["Name"].get(),
                lname=fields["Last Name"].get(),
                ncode=fields["National Code"].get(),
                age=int(fields["Age"].get()),
                phone=fields["Phone"].get(),
                address=fields["Address"].get(),
                salary=int(fields["Salary"].get()),
                shift=fields["Shift"].get(),
                edu_level=fields["Education Level"].get(),
                major=fields["Major"].get(),
                work_experience=int(fields["Work Experience"].get())
            )

            emp_type = emp_type_var.get()

            # ❗ add داخل constructor انجام میشه — اینجا دوباره add نزن

            if emp_type == "SchoolManager":
                SchoolManager(
                    **common,
                    license_number=fields["License Number"].get(),
                    room_number=int(fields["Room Number"].get())
                )

            elif emp_type == "AssistantPrincipal":
                AssistantPrincipal(
                    **common,
                    department=fields["Department"].get(),
                    teaching_hours=int(fields["Teaching Hours"].get())
                )

            elif emp_type == "Teacher":
                Teacher(
                    **common,
                    subject_name=fields["Subject Name"].get(),
                    teaching_hours=int(fields["Teaching Hours"].get()),
                    teaching_days=int(fields["Teaching Days"].get()),
                    overtime_hours=int(fields["Overtime Hours"].get())
                )

            else:
                Janitor(**common, duties=fields["Duties"].get())

            messagebox.showinfo("Success", "Employee added successfully")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Save Employee",
              width=25, command=save_employee).pack(pady=5)
    tk.Button(win, text="Close",
              width=25, command=win.destroy).pack(pady=5)


# ========================== EDIT ==========================
def edit_employee(root=None):
    win = tk.Toplevel(root)
    win.title("Edit Employee")
    win.geometry("500x800")
    win.grab_set()

    tk.Label(win, text="Employee ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    form_frame = tk.Frame(win)
    form_frame.pack(pady=10)
    fields = {}

    def search_and_edit():
        try:
            emp_id = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid ID")
            return

        emp = SchoolEmployee.search_by_id(emp_id)
        if not emp:
            messagebox.showerror("Error", "Employee not found")
            return

        for w in form_frame.winfo_children():
            w.destroy()
        fields.clear()

        def add_field(label, value="", is_combo=False, values=None):
            tk.Label(form_frame, text=label).pack()

            if is_combo:
                e = ttk.Combobox(form_frame, values=values, state="readonly")
                e.set(value)
            else:
                e = tk.Entry(form_frame)
                e.insert(0, str(value))

            e.pack()
            fields[label] = e

        # ---------- common fields ----------
        add_field("Name", emp.name)
        add_field("Last Name", emp.lname)
        add_field("National Code", emp.ncode)
        add_field("Age", emp.age)
        add_field("Phone", emp.phone)
        add_field("Address", emp.address)
        add_field("Salary", emp.salary)

        add_field("Shift", emp.shift, True, SHIFT_OPTIONS)
        add_field("Education Level", emp.edu_level, True, EDU_OPTIONS)

        add_field("Major", emp.major)
        add_field("Work Experience", emp.work_experience)

        # ---------- save ----------
        def do_edit():
            try:
                emp.name = fields["Name"].get()
                emp.lname = fields["Last Name"].get()
                emp.ncode = fields["National Code"].get()
                emp.age = int(fields["Age"].get())
                emp.phone = fields["Phone"].get()
                emp.address = fields["Address"].get()
                emp.salary = int(fields["Salary"].get())
                emp.shift = fields["Shift"].get()
                emp.edu_level = fields["Education Level"].get()
                emp.major = fields["Major"].get()
                emp.work_experience = int(fields["Work Experience"].get())

                emp.edit()

                messagebox.showinfo("Success", "Employee edited successfully")
                win.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(form_frame, text="Save Edit",
                  width=25, command=do_edit).pack(pady=10)

    tk.Button(win, text="Search", width=25, command=search_and_edit).pack(pady=5)
    tk.Button(win, text="Close", width=25, command=win.destroy).pack(pady=5)



# ========================== REMOVE ==========================
def remove_employee(root=None):
    win = tk.Toplevel(root)
    win.title("Remove Employee")
    win.geometry("400x200")
    win.grab_set()

    tk.Label(win, text="Employee ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    def do_remove():
        try:
            emp_id = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid ID")
            return

        emp = SchoolEmployee.search_by_id(emp_id)
        if not emp:
            messagebox.showerror("Error", "Employee not found")
            return

        emp.remove()
        messagebox.showinfo("Success", "Employee removed")
        win.destroy()

    tk.Button(win, text="Remove",
              width=25, command=do_remove).pack(pady=10)
    tk.Button(win, text="Close",
              width=25, command=win.destroy).pack()


# ========================== SHOW ALL ==========================
def show_all_employees(root=None):
    win = tk.Toplevel(root)
    win.title("All Employees")
    win.geometry("800x400")

    listbox = tk.Listbox(win, width=130)
    listbox.pack(fill="both", expand=True)

    for info in SchoolEmployee.show_all():
        listbox.insert(tk.END, info)

    tk.Button(win, text="Close",
              command=win.destroy).pack(pady=5)


# ========================== SEARCH ==========================
def search_employee(root=None):
    win = tk.Toplevel(root)
    win.title("Search Employee")
    win.geometry("500x400")
    win.grab_set()

    tk.Label(win, text="Employee ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    result_label = tk.Label(win, text="", justify="left")
    result_label.pack(pady=10)

    def do_search():
        try:
            emp_id = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid ID")
            return

        emp = SchoolEmployee.search_by_id(emp_id)
        if not emp:
            messagebox.showerror("Error", "Employee not found")
            return

        info = (
            f"ID: {emp.em_id}\n"
            f"Name: {emp.name} {emp.lname}\n"
            f"National Code: {emp.ncode}\n"
            f"Age: {emp.age}\n"
            f"Phone: {emp.phone}\n"
            f"Address: {emp.address}\n"
            f"Role: {emp.role}\n"
            f"Salary: {emp.salary}"
        )

        result_label.config(text=info)

    tk.Button(win, text="Search",
              width=25, command=do_search).pack(pady=5)
    tk.Button(win, text="Close",
              width=25, command=win.destroy).pack(pady=5)
