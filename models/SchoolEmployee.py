from database.db import get_connection
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "log")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "School_Manager_System_log.txt")


def write_log(message: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time}] {message}\n")


# ================= BASE CLASS =================
class SchoolEmployee:

    def __init__(
        self, name, lname, ncode, age, phone, address,
        salary, role, shift, edu_level, major, work_experience,
        em_id=None
    ):
        self.__em_id = em_id
        self.name = name
        self.lname = lname
        self.ncode = ncode
        self.age = age
        self.phone = phone
        self.address = address
        self.salary = salary
        self.role = role
        self.shift = shift
        self.edu_level = edu_level
        self.major = major
        self.work_experience = work_experience

    # ---------- properties ----------
    @property
    def em_id(self):
        return self.__em_id

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value <= 0:
            raise ValueError("Invalid salary")
        self.__salary = value

    # ---------- ADD ----------
    def add(self, **extra):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO employees
                (name, lname, ncode, age, phone, address,
                 salary, role, shift, edu_level, major, work_experience,
                 license_number, room_number,
                 department, teaching_hours,
                 subject_name, teaching_days, overtime_hours,
                 duties)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                self.name, self.lname, self.ncode, self.age,
                self.phone, self.address,
                self.salary, self.role, self.shift,
                self.edu_level, self.major, self.work_experience,

                extra.get("license_number"),
                extra.get("room_number"),

                extra.get("department"),
                extra.get("teaching_hours"),

                extra.get("subject_name"),
                extra.get("teaching_days"),
                extra.get("overtime_hours"),

                extra.get("duties")
            ))

            self.__em_id = cursor.lastrowid
            conn.commit()

        write_log(f"Employee added (id : {self.em_id})")

    # ---------- REMOVE ----------
    def remove(self):
        if not self.em_id:
            return

        with get_connection() as conn:
            conn.execute("DELETE FROM employees WHERE em_id = ?", (self.em_id,))
            conn.commit()

        write_log(f"Employee removed (id : {self.em_id})")

    # ---------- EDIT ----------
    def edit(self, **extra):
        with get_connection() as conn:
            conn.execute("""
                UPDATE employees SET
                name=?, lname=?, ncode=?, age=?, phone=?, address=?,
                salary=?, shift=?, edu_level=?, major=?, work_experience=?,
                license_number=?, room_number=?,
                department=?, teaching_hours=?,
                subject_name=?, teaching_days=?, overtime_hours=?,
                duties=?
                WHERE em_id=?
            """, (
                self.name, self.lname, self.ncode, self.age,
                self.phone, self.address,
                self.salary, self.shift,
                self.edu_level, self.major, self.work_experience,

                extra.get("license_number"),
                extra.get("room_number"),

                extra.get("department"),
                extra.get("teaching_hours"),

                extra.get("subject_name"),
                extra.get("teaching_days"),
                extra.get("overtime_hours"),

                extra.get("duties"),

                self.em_id
            ))
            conn.commit()

        write_log(f"Employee edited (id : {self.em_id})")

    # ---------- SEARCH ----------
    @classmethod
    def search_by_id(cls, emp_id):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM employees WHERE em_id=?",
                (emp_id,)
            ).fetchone()

        if not row:
            return None

        return cls._row_to_object(row)

    # ---------- SHOW ALL ----------
    @classmethod
    def show_all(cls):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT em_id, role, name, lname, salary FROM employees"
            ).fetchall()

        return [
            f"ID:{r[0]} - Role: {r[1]} - Name: {r[2]} {r[3]} - Salary: {r[4]}"
            for r in rows
        ]

    # ---------- ROW TO OBJECT ----------
    @staticmethod
    def _row_to_object(row):

        (
            em_id, name, lname, ncode, age, phone, address,
            salary, role, shift, edu_level, major, work_experience,
            license_number, room_number,
            department, teaching_hours,
            subject_name, teaching_days, overtime_hours,
            duties
        ) = row

        if role == "Manager":
            return SchoolManager(
                name, lname, ncode, age, phone, address,
                salary, shift, edu_level, major, work_experience,
                license_number, room_number,
                em_id
            )

        elif role == "Teacher":
            return Teacher(
                name, lname, ncode, age, phone, address,
                salary, shift, edu_level, major, work_experience,
                subject_name, teaching_hours, teaching_days, overtime_hours,
                em_id
            )

        elif role == "Assistant":
            return AssistantPrincipal(
                name, lname, ncode, age, phone, address,
                salary, shift, edu_level, major, work_experience,
                department, teaching_hours,
                em_id
            )

        elif role == "Janitor":
            return Janitor(
                name, lname, ncode, age, phone, address,
                salary, shift, edu_level, major, work_experience,
                duties,
                em_id
            )

        return None


# ================= CHILD CLASSES =================

class SchoolManager(SchoolEmployee):
    def __init__(self, name, lname, ncode, age, phone, address,
                 salary, shift, edu_level, major, work_experience,
                 license_number, room_number, em_id=None):

        super().__init__(
            name, lname, ncode, age, phone, address,
            salary, "Manager", shift, edu_level, major, work_experience,
            em_id
        )

        self.license_number = license_number
        self.room_number = room_number


class Teacher(SchoolEmployee):
    def __init__(self, name, lname, ncode, age, phone, address,
                 salary, shift, edu_level, major, work_experience,
                 subject_name, teaching_hours, teaching_days, overtime_hours,
                 em_id=None):

        super().__init__(
            name, lname, ncode, age, phone, address,
            salary, "Teacher", shift, edu_level, major, work_experience,
            em_id
        )

        self.subject_name = subject_name
        self.teaching_hours = teaching_hours
        self.teaching_days = teaching_days
        self.overtime_hours = overtime_hours


class AssistantPrincipal(SchoolEmployee):
    def __init__(self, name, lname, ncode, age, phone, address,
                 salary, shift, edu_level, major, work_experience,
                 department, teaching_hours, em_id=None):

        super().__init__(
            name, lname, ncode, age, phone, address,
            salary, "Assistant", shift, edu_level, major, work_experience,
            em_id
        )

        self.department = department
        self.teaching_hours = teaching_hours


class Janitor(SchoolEmployee):
    def __init__(self, name, lname, ncode, age, phone, address,
                 salary, shift, edu_level, major, work_experience,
                 duties, em_id=None):

        super().__init__(
            name, lname, ncode, age, phone, address,
            salary, "Janitor", shift, edu_level, major, work_experience,
            em_id
        )

        self.duties = duties
