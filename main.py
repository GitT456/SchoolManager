from database.db import init_db
import tkinter as tk
from tkinter import messagebox
import sys
import os
from datetime import datetime
from ui.Student_ui import *
from ui.Subject_ui import *
from ui.ClassRoom_ui import *
from ui.SchoolEmployee_ui import *
from ui.lib_item_ui import *
from ui.member_ui import *

# ================== Helper ==================
def resource_path(relative_path):
    """
    پیدا کردن مسیر صحیح منابع برای PyInstaller
    """
    try:
        base_path = sys._MEIPASS  # وقتی PyInstaller همه چیز رو بسته بندی کرد
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================== Logging ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "School_Manager_System_log.txt")

def write_log(message: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time}] {message}\n")

# ================== GUI ==================
root = tk.Tk()
root.title("School Manager System")
root.state("zoomed")
root.configure(bg="#e5e7eb")

# ---------- Main Layout ----------
container = tk.Frame(root, bg="#e5e7eb")
container.pack(fill="both", expand=True)

# ---------- Left (Background Image) ----------
left_frame = tk.Frame(container, bg="#e5e7eb")
left_frame.pack(side="left", fill="both", expand=True)

bg_image_path = resource_path("images/background.png")
if os.path.exists(bg_image_path):
    bg_image = tk.PhotoImage(file=bg_image_path)
    bg_label = tk.Label(left_frame, image=bg_image, bg="#e5e7eb")
    bg_label.place(relx=0.5, rely=0.5, anchor="center")
else:
    tk.Label(left_frame, text="Background Image Not Found",
             font=("Arial", 20), bg="#e5e7eb").pack(expand=True)

# ---------- Right (Menu) ----------
menu_frame = tk.Frame(container, bg="#0f172a", width=420)
menu_frame.pack(side="right", fill="y")
menu_frame.pack_propagate(False)

# ================== Utils ==================
def clear_menu():
    for w in menu_frame.winfo_children():
        w.destroy()

def menu_btn(text, cmd):
    btn = tk.Button(
        menu_frame,
        text=text,
        command=cmd,
        font=("Segoe UI", 11, "bold"),
        bg="#1e293b",
        fg="white",
        activebackground="#334155",
        activeforeground="white",
        bd=0,
        height=2,
        cursor="hand2"
    )
    def on_enter(e):
        btn['bg'] = 'white'
        btn['fg'] = 'black'
    def on_leave(e):
        btn['bg'] = '#1e293b'
        btn['fg'] = 'white'
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def title(text):
    tk.Label(
        menu_frame,
        text=text,
        font=("Segoe UI", 18, "bold"),
        bg="#0f172a",
        fg="white"
    ).pack(pady=25)

def back_btn(cmd):
    btn = tk.Button(
        menu_frame,
        text="Back",
        command=cmd,
        font=("Segoe UI", 11, "bold"),
        bg="#3b82f6",
        fg="white",
        activebackground="#2563eb",
        bd=0,
        height=2,
        cursor="hand2"
    )
    def on_enter(e):
        btn['bg'] = 'white'
        btn['fg'] = 'black'
    def on_leave(e):
        btn['bg'] = '#3b82f6'
        btn['fg'] = 'white'
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(fill="x", padx=30, pady=20)

# ================== Menu Functions ==================
# Library
def Items_Management():
    clear_menu()
    title("Items Management")
    menu_btn("Add", add_item).pack(fill="x", padx=30, pady=5)
    menu_btn("Remove", remove_item).pack(fill="x", padx=30, pady=5)
    menu_btn("Search", search_item).pack(fill="x", padx=30, pady=5)
    menu_btn("Edit", edit_item).pack(fill="x", padx=30, pady=5)
    menu_btn("Show All", show_all_items).pack(fill="x", padx=30, pady=5)
    back_btn(Library_Management)

def Register_Management():
    clear_menu()
    title("Register Management")
    menu_btn("Add", add_member).pack(fill="x", padx=30, pady=5)
    menu_btn("Remove", remove_member).pack(fill="x", padx=30, pady=5)
    menu_btn("Search", search_member).pack(fill="x", padx=30, pady=5)
    menu_btn("Edit", edit_member).pack(fill="x", padx=30, pady=5)
    menu_btn("Show All", show_all_members).pack(fill="x", padx=30, pady=5)
    back_btn(Library_Management)

def Library_Management():
    clear_menu()
    title("Library Management")
    menu_btn("Items", Items_Management).pack(fill="x", padx=30, pady=6)
    menu_btn("Register", Register_Management).pack(fill="x", padx=30, pady=6)
    back_btn(main_menu)

# Student
def Student_Management_m():
    clear_menu()
    title("Student Management")
    menu_btn("Add", add_student).pack(fill="x", padx=30, pady=5)
    menu_btn("Remove", remove_student).pack(fill="x", padx=30, pady=5)
    menu_btn("Search", search_student).pack(fill="x", padx=30, pady=5)
    menu_btn("Edit", edit_student).pack(fill="x", padx=30, pady=5)
    menu_btn("Show All", show_all_students).pack(fill="x", padx=30, pady=5)
    back_btn(main_menu)

# Subject
def Subject_Management():
    clear_menu()
    title("Subject Management")
    menu_btn("Add", add_subject).pack(fill="x", padx=30, pady=5)
    menu_btn("Remove", remove_subject).pack(fill="x", padx=30, pady=5)
    menu_btn("Search", search_subject).pack(fill="x", padx=30, pady=5)
    menu_btn("Edit", edit_subject).pack(fill="x", padx=30, pady=5)
    menu_btn("Show All", show_all_subjects).pack(fill="x", padx=30, pady=5)
    back_btn(main_menu)

# Classroom
def ClassRoom_Management():
    clear_menu()
    title("Classroom Management")
    menu_btn("Add", add_classroom).pack(fill="x", padx=30, pady=5)
    menu_btn("Remove", remove_classroom).pack(fill="x", padx=30, pady=5)
    menu_btn("Search", search_classroom).pack(fill="x", padx=30, pady=5)
    menu_btn("Edit", edit_classroom).pack(fill="x", padx=30, pady=5)
    menu_btn("Show All", show_all_classrooms).pack(fill="x", padx=30, pady=5)
    back_btn(main_menu)

# School Employee
def SchoolEmployee_Management():
    clear_menu()
    title("School Employee Management")
    menu_btn("Add", add_employee).pack(fill="x", padx=30, pady=5)
    menu_btn("Remove", remove_employee).pack(fill="x", padx=30, pady=5)
    menu_btn("Search", search_employee).pack(fill="x", padx=30, pady=5)
    menu_btn("Edit", edit_employee).pack(fill="x", padx=30, pady=5)
    menu_btn("Show All", show_all_employees).pack(fill="x", padx=30, pady=5)
    back_btn(main_menu)

# ================== Main Menu ==================
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        write_log("Application closed by user.")
        root.destroy()

# ================== Main Menu ==================
def main_menu():
    clear_menu()
    title("School Manager System")
    menu_btn("Student", Student_Management_m).pack(fill="x", padx=30, pady=6)
    menu_btn("Subject", Subject_Management).pack(fill="x", padx=30, pady=6)
    menu_btn("ClassRoom", ClassRoom_Management).pack(fill="x", padx=30, pady=6)
    menu_btn("School Employee", SchoolEmployee_Management).pack(fill="x", padx=30, pady=6)
    menu_btn("Library Management", Library_Management).pack(fill="x", padx=30, pady=6)

    exit_btn = tk.Button(
        menu_frame,
        text="Exit",
        command=exit_app,
        font=("Segoe UI", 11, "bold"),
        bg="#ef4444",
        fg="white",
        activebackground="#dc2626",
        bd=0,
        height=2,
        cursor="hand2"
    )
    def on_enter(e):
        exit_btn['bg'] = 'white'
        exit_btn['fg'] = 'black'
    def on_leave(e):
        exit_btn['bg'] = '#ef4444'
        exit_btn['fg'] = 'white'
    exit_btn.bind("<Enter>", on_enter)
    exit_btn.bind("<Leave>", on_leave)
    exit_btn.pack(fill="x", padx=30, pady=30)

# ================== Start ==================
if __name__ == '__main__':
    init_db()
    write_log("Application started.")
    main_menu()
    root.mainloop()
