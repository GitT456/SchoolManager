from datetime import datetime
import os
from database.db import get_connection

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
class Subject:

    def __init__(self, subject_name, subject_teacher, subject_grade, subject_category, subject_id=None):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.subject_teacher = subject_teacher
        self.subject_grade = subject_grade
        self.subject_category = subject_category

        if self.subject_id is None:
            self.add()

    # ---------- CRUD ----------
    def add(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO subjects (subject_name, subject_teacher, subject_grade, subject_category)
                VALUES (?, ?, ?, ?)
            """, (self.subject_name, self.subject_teacher, self.subject_grade, self.subject_category))
            self.subject_id = cursor.lastrowid
            conn.commit()

        write_log(f"Subject ===> Added (id : {self.subject_id})")

    def remove(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (self.subject_id,))
            conn.commit()

        write_log(f"Subject ===> Removed (id : {self.subject_id})")

    def edit(self, n_subject_name=None, n_subject_teacher=None, n_subject_grade=None, n_subject_category=None):
        if n_subject_name is not None:
            self.subject_name = n_subject_name
        if n_subject_teacher is not None:
            self.subject_teacher = n_subject_teacher
        if n_subject_grade is not None:
            self.subject_grade = n_subject_grade
        if n_subject_category is not None:
            self.subject_category = n_subject_category

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE subjects
                SET subject_name=?, subject_teacher=?, subject_grade=?, subject_category=?
                WHERE subject_id=?
            """, (self.subject_name, self.subject_teacher, self.subject_grade, self.subject_category, self.subject_id))
            conn.commit()

        write_log(f"Subject ===> Edited (id : {self.subject_id})")

    def show(self):
        write_log(f"Subject ===> Info requested (id : {self.subject_id})")
        return (
            f"Subject ID: {self.subject_id}\n"
            f"Name: {self.subject_name}\n"
            f"Teacher: {self.subject_teacher}\n"
            f"Grade: {self.subject_grade}\n"
            f"Category: {self.subject_category}"
        )

    # ---------- CLASS METHODS ----------
    @classmethod
    def search_by_id(cls, subject_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
            row = cursor.fetchone()

        if row:
            write_log(f"Subject ===> Search success (id : {subject_id})")
            return cls(subject_id=row[0], subject_name=row[1], subject_teacher=row[2], subject_grade=row[3], subject_category=row[4])

        write_log(f"Subject ===> Search failed (id : {subject_id})")
        return None

    @classmethod
    def show_all(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects")
            rows = cursor.fetchall()

        write_log("Subject ===> Show all requested")
        return [
            f"ID: {r[0]} - Name: {r[1]} - Teacher: {r[2]} - Grade: {r[3]} - Category: {r[4]}"
            for r in rows
        ]

    @classmethod
    def get_subject_list(cls):
        """لیست دروس به صورت دیکشنری برای UI"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT subject_id, subject_name FROM subjects")
            rows = cursor.fetchall()
        return [{"subject_id": r[0], "subject_name": r[1]} for r in rows]

    @classmethod
    def subject_count(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM subjects")
            count = cursor.fetchone()[0]
        write_log(f"Subject ===> Count requested (total : {count})")
        return count
