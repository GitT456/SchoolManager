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
class ClassRoom:

    def __init__(self, class_name, class_grade, capacity=30, class_id=None):
        self.class_id = class_id
        self.class_name = class_name
        self.class_grade = class_grade
        self.capacity = capacity

        if self.class_id is None:
            self.add()

    # ---------- VALIDATION ----------
    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if 1 <= value <= 30:
            self.__capacity = value
        else:
            raise ValueError("Invalid capacity")

    @property
    def class_grade(self):
        return self.__class_grade

    @class_grade.setter
    def class_grade(self, value):
        if 7 <= value <= 9:
            self.__class_grade = value
        else:
            raise ValueError("Invalid class grade")

    # ---------- CRUD ----------
    def add(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO classrooms (class_name, class_grade, capacity)
                VALUES (?, ?, ?)
            """, (self.class_name, self.class_grade, self.capacity))
            self.class_id = cursor.lastrowid
            conn.commit()

        write_log(f"ClassRoom ===> Added (id : {self.class_id})")

    def remove(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM classrooms WHERE class_id = ?", (self.class_id,))
            conn.commit()

        write_log(f"ClassRoom ===> Removed (id : {self.class_id})")

    def edit(self, class_name=None, n_class_grade=None, n_capacity=None):
        if class_name is not None:
            self.class_name = class_name
        if n_class_grade is not None:
            self.class_grade = n_class_grade
        if n_capacity is not None:
            self.capacity = n_capacity

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE classrooms
                SET class_name=?, class_grade=?, capacity=?
                WHERE class_id=?
            """, (self.class_name, self.class_grade, self.capacity, self.class_id))
            conn.commit()

        write_log(f"ClassRoom ===> Edited (id : {self.class_id})")

    def show(self):
        write_log(f"ClassRoom ===> Info requested (id : {self.class_id})")
        return (
            f"Class Room ID: {self.class_id}\n"
            f"Class Room Name: {self.class_name}\n"
            f"Class Room Grade: {self.class_grade}\n"
            f"Class Room Capacity: {self.capacity}"
        )

    # ---------- CLASS METHODS ----------
    @classmethod
    def search_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classrooms WHERE class_id = ?", (id,))
            row = cursor.fetchone()

        if row:
            write_log(f"ClassRoom ===> Search success (id : {id})")
            return cls(class_id=row[0], class_name=row[1], class_grade=row[2], capacity=row[3])

        write_log(f"ClassRoom ===> Search failed (id : {id})")
        return None

    @classmethod
    def show_all(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classrooms")
            rows = cursor.fetchall()

        write_log("ClassRoom ===> Show all requested")
        return [
            f"ID: {r[0]} - Name: {r[1]} - Grade: {r[2]} - Capacity: {r[3]}"
            for r in rows
        ]

    @classmethod
    def get_class_list(cls):
        """لیست کلاس‌ها را به صورت لیست دیکشنری برمی‌گرداند"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT class_id, class_name FROM classrooms")
            rows = cursor.fetchall()

        return [{"class_id": r[0], "class_name": r[1]} for r in rows]

    @classmethod
    def classroom_count(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM classrooms")
            count = cursor.fetchone()[0]

        write_log(f"ClassRoom ===> Count requested (total : {count})")
        return count
