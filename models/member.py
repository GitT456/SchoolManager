from datetime import datetime
import os
import sqlite3
from database.db import get_connection
from models.Person import Person

# ---------- LOG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "School_Manager_System_log.txt")

def write_log(message: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time}] {message}\n")


# ---------- CLASS MEMBER ----------
class Member(Person):

    def __init__(self, name, lname, ncode, age, phone, address, membership_num, username=None, password=None, add_to_db=True):
        super().__init__(name, lname, ncode, age, phone, address)
        self.membership_num = membership_num
        self.username = username
        self.password = password
        if add_to_db:
            self.add()

    # ---------- CRUD ----------
    def add(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO members (name, lname, ncode, age, phone, address, membership_num, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.name, self.lname, self.ncode, self.age, self.phone, self.address,
                  self.membership_num, self.username, self.password))
            conn.commit()
            conn.close()
            write_log(f"Member ===> Added (membership_num: {self.membership_num})")
        except Exception as e:
            write_log(f"Member ===> Add FAILED (membership_num: {self.membership_num}) - {e}")
            raise e

    def remove(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM members WHERE membership_num=?", (self.membership_num,))
            conn.commit()
            conn.close()
            write_log(f"Member ===> Removed (membership_num: {self.membership_num})")
        except Exception as e:
            write_log(f"Member ===> Remove FAILED (membership_num: {self.membership_num}) - {e}")
            raise e

    def edit(self, n_name=None, n_lname=None, n_ncode=None, n_age=None, n_phone=None, n_address=None,
             n_membership_num=None, n_username=None, n_password=None):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            updates = []
            params = []

            old_membership = self.membership_num  # برای شرط WHERE

            if n_name is not None:
                updates.append("name=?"); params.append(n_name); self.name = n_name
            if n_lname is not None:
                updates.append("lname=?"); params.append(n_lname); self.lname = n_lname
            if n_ncode is not None:
                updates.append("ncode=?"); params.append(n_ncode); self.ncode = n_ncode
            if n_age is not None:
                updates.append("age=?"); params.append(n_age); self.age = n_age
            if n_phone is not None:
                updates.append("phone=?"); params.append(n_phone); self.phone = n_phone
            if n_address is not None:
                updates.append("address=?"); params.append(n_address); self.address = n_address
            if n_membership_num is not None:
                updates.append("membership_num=?"); params.append(n_membership_num); self.membership_num = n_membership_num
            if n_username is not None:
                updates.append("username=?"); params.append(n_username); self.username = n_username
            if n_password is not None:
                updates.append("password=?"); params.append(n_password); self.password = n_password

            if updates:
                params.append(old_membership)
                cursor.execute(f"UPDATE members SET {', '.join(updates)} WHERE membership_num=?", params)
                conn.commit()

            conn.close()
            write_log(f"Member ===> Edited (membership_num: {self.membership_num})")
        except Exception as e:
            write_log(f"Member ===> Edit FAILED (membership_num: {self.membership_num}) - {e}")
            raise e

    # ---------- CLASS METHODS ----------
    @classmethod
    def search_by_membership_num(cls, membership_num):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, lname, ncode, age, phone, address, membership_num, username, password
            FROM members WHERE membership_num=?
        """, (membership_num,))
        row = cursor.fetchone()
        conn.close()

        if row:
            member = Member(*row[:6], membership_num=row[6], username=row[7], password=row[8], add_to_db=False)
            write_log(f"Member ===> Search success (membership_num: {membership_num})")
            return member
        else:
            write_log(f"Member ===> Search failed (membership_num: {membership_num})")
            return None

    @classmethod
    def show_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, lname, ncode, age, phone, address, membership_num, username, password FROM members")
        rows = cursor.fetchall()
        conn.close()

        members_info = []
        for row in rows:
            info = f"membership_num: {row[6]}, Name: {row[0]} {row[1]}, National Code: {row[2]}"
            members_info.append(info)

        write_log("Member ===> Show all items requested")
        return members_info
