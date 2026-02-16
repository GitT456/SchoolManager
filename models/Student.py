from models.Person import Person
from database.db import get_connection
from datetime import datetime
import os

# ---------- LOG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "School_Manager_System_log.txt")

def write_log(message: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time}] {message}\n")


# ---------- MODEL ----------
class Student(Person):

    def __init__(self, classroom_id, name, lname, ncode, age, phone, address, grade, student_id=None):
        self.student_id = student_id
        self.classroom_id = classroom_id
        self.grade = grade
        super().__init__(name, lname, ncode, age, phone, address)

        if self.student_id is None:
            self.add()

    # ---------- CRUD ----------
    def add(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (classroom_id, name, lname, ncode, age, phone, address, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.classroom_id, self.name, self.lname, self.ncode,
                  self.age, self.phone, self.address, self.grade))
            self.student_id = cursor.lastrowid
            conn.commit()
        write_log(f"Student ===> Added (id : {self.student_id})")

    def remove(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?", (self.student_id,))
            conn.commit()
        write_log(f"Student ===> Removed (id : {self.student_id})")

    def edit(self, n_classroom_id=None, n_name=None, n_lname=None, n_ncode=None,
             n_age=None, n_phone=None, n_address=None, n_grade=None):
        if n_classroom_id is not None:
            self.classroom_id = n_classroom_id
        if n_name is not None:
            self.name = n_name
        if n_lname is not None:
            self.lname = n_lname
        if n_ncode is not None:
            self.ncode = n_ncode
        if n_age is not None:
            self.age = n_age
        if n_phone is not None:
            self.phone = n_phone
        if n_address is not None:
            self.address = n_address
        if n_grade is not None:
            self.grade = n_grade

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students
                SET classroom_id=?, name=?, lname=?, ncode=?, age=?, phone=?, address=?, grade=?
                WHERE student_id=?
            """, (self.classroom_id, self.name, self.lname, self.ncode, self.age,
                  self.phone, self.address, self.grade, self.student_id))
            conn.commit()
        write_log(f"Student ===> Edited (id : {self.student_id})")

    def show(self):
        write_log(f"Student ===> Info requested (id : {self.student_id})")
        return (
            f"Student ID: {self.student_id}\n"
            f"Name: {self.name}\n"
            f"Last Name: {self.lname}\n"
            f"National Code: {self.ncode}\n"
            f"Age: {self.age}\n"
            f"Phone: {self.phone}\n"
            f"Address: {self.address}\n"
            f"Classroom ID: {self.classroom_id}\n"
            f"Grade: {self.grade}"
        )

    # ---------- CLASS METHODS ----------
    @classmethod
    def search_by_id(cls, student_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            row = cursor.fetchone()
        if row:
            write_log(f"Student ===> Search success (id : {student_id})")
            return cls(student_id=row[0], classroom_id=row[1], name=row[2], lname=row[3],
                       ncode=row[4], age=row[5], phone=row[6], address=row[7], grade=row[8])
        write_log(f"Student ===> Search failed (id : {student_id})")
        return None

    @classmethod
    def show_all(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
        write_log("Student ===> Show all requested")
        return [
            f"ID: {r[0]} - {r[2]} {r[3]} - Grade: {r[8]} - Age: {r[5]}"
            for r in rows
        ]

    @classmethod
    def student_count(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
        write_log(f"Student ===> Count requested (total : {count})")
        return count
