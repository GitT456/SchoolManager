import os
import sqlite3

# ---------- مسیر پروژه ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "school.db")


# ---------- اتصال ----------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------- ایجاد جداول ----------
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # ================= ClassRoom =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS classrooms (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            class_grade INTEGER NOT NULL,
            capacity INTEGER NOT NULL
        )
        """)

        # ================= Student =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            classroom_id INTEGER,
            name TEXT NOT NULL,
            lname TEXT NOT NULL,
            ncode TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            phone TEXT,
            address TEXT,
            grade INTEGER NOT NULL,
            FOREIGN KEY (classroom_id)
                REFERENCES classrooms(class_id)
                ON DELETE SET NULL
        )
        """)

        # ================= Library Items =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            year INTEGER,
            type TEXT NOT NULL,        -- Book / Magazine / DVD
            author TEXT,
            isbn TEXT,
            num_page INTEGER,
            duration INTEGER,
            num_file INTEGER
        )
        """)

        # ================= Members =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lname TEXT NOT NULL,
            ncode TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            phone TEXT,
            address TEXT,
            membership_num TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        # ================= Subjects =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            teacher_id INTEGER,
            subject_grade INTEGER NOT NULL,
            subject_category TEXT
        )
        """)

        # ================= Employees =================
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS employees
                       (
                           em_id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT
                           NOT
                           NULL,
                           lname
                           TEXT
                           NOT
                           NULL,
                           ncode
                           TEXT
                           NOT
                           NULL,
                           age
                           INTEGER
                           NOT
                           NULL,
                           phone
                           TEXT,
                           address
                           TEXT,
                           salary
                           INTEGER
                           NOT
                           NULL,
                           role
                           TEXT
                           NOT
                           NULL, -- manager / assistant / teacher / janitor
                           shift
                           TEXT,
                           edu_level
                           TEXT,
                           major
                           TEXT,
                           work_experience
                           INTEGER,

                           -- SchoolManager
                           license_number
                           TEXT,
                           room_number
                           INTEGER,

                           -- AssistantPrincipal
                           department
                           TEXT,
                           teaching_hours
                           INTEGER,

                           -- Teacher
                           subject_name
                           TEXT,
                           teaching_days
                           INTEGER,
                           overtime_hours
                           INTEGER,

                           -- Janitor
                           duties
                           TEXT
                       )
                       """)

        conn.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully ✔")
    print("Tables: classrooms, students, subjects, items, members")
