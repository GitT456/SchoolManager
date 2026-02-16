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


class Item:
    Item_list = []  # فقط برای سازگاری – استفاده نمی‌شود

    def __init__(self, name, price, category, year, item_type,
                 author=None, isbn=None, num_page=None,
                 duration=None, num_file=None):

        self.__id = None
        self.name = name
        self.price = price
        self.category = category
        self.year = year
        self.type = item_type
        self.author = author
        self.isbn = isbn
        self.num_page = num_page
        self.duration = duration
        self.num_file = num_file



    @property
    def id(self):
        return self.__id

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

    def add(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO items 
            (name, price, category, year, type, author, isbn, num_page, duration, num_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.name, self.price, self.category, self.year,
                self.type, self.author, self.isbn,
                self.num_page, self.duration, self.num_file
            ))
            self.__id = cursor.lastrowid
            conn.commit()

        write_log(f"Library Item ===> Item added (id : {self.id})")

    def remove(self):
        with get_connection() as conn:
            conn.execute("DELETE FROM items WHERE id = ?", (self.id,))
            conn.commit()
        write_log(f"Library Item ===> Item removed (id : {self.id})")

    @classmethod
    def search_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
            row = cursor.fetchone()

        if not row:
            write_log(f"Library Item ===> Search failed (id : {id})")
            return None

        return cls._row_to_object(row)

    @classmethod
    def show_all(cls):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM items").fetchall()

        result = []
        for row in rows:
            i = cls._row_to_object(row)
            info = f"Found ==> ID: {i.id} - name: {i.name} - category: {i.category} - price: {i.price} - year: {i.year}"
            result.append(info)
        write_log("Library Item ===> Show all items requested")
        return result

    @classmethod
    def Item_count(cls):
        with get_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        write_log(f"Library Item ===> Count requested (total : {count})")
        print(f"Item count is: {count}")

    def edit(self, n_name=None, n_price=None, n_category=None, n_year=None,
             n_author=None, n_isbn=None, n_page_num=None,
             n_duration=None, n_num_file=None):

        if n_name: self.name = n_name
        if n_price is not None: self.price = n_price
        if n_category: self.category = n_category
        if n_year: self.year = n_year

        if hasattr(self, "author") and n_author is not None:
            self.author = n_author
        if hasattr(self, "isbn") and n_isbn is not None:
            self.isbn = n_isbn
        if hasattr(self, "num_page") and n_page_num is not None:
            self.num_page = n_page_num
        if hasattr(self, "duration") and n_duration is not None:
            self.duration = n_duration
        if hasattr(self, "num_file") and n_num_file is not None:
            self.num_file = n_num_file

        # بروزرسانی دیتابیس
        with get_connection() as conn:
            conn.execute("""
                         UPDATE items
                         SET name=?,
                             price=?,
                             category=?,
                             year=?,
                             author=?,
                             isbn=?,
                             num_page=?,
                             duration=?,
                             num_file=?
                         WHERE id = ?
                         """, (self.name, self.price, self.category, self.year,
                               getattr(self, "author", None), getattr(self, "isbn", None),
                               getattr(self, "num_page", None), getattr(self, "duration", None),
                               getattr(self, "num_file", None), self.id))
            conn.commit()

        write_log(f"Library Item ===> Item edited (id : {self.id})")

    @staticmethod
    def _row_to_object(row):
        _, name, price, category, year, type_, author, isbn, num_page, duration, num_file = row

        if type_ == "Book":
            obj = Book(name, price, category, year, author, isbn, num_page)
        elif type_ == "Magazine":
            obj = Magazine(name, price, category, year, num_page)
        elif type_ == "DVD":
            obj = DVD(name, price, category, year, duration, num_file)
        else:
            return None

        obj.__id = row[0]
        return obj


class Book(Item):
    def __init__(self, name, price, category, year, author, isbn, num_page):
        super().__init__(name, price, category, year, "Book",
                         author=author, isbn=isbn, num_page=num_page)


class Magazine(Item):
    def __init__(self, name, price, category, year, num_page):
        super().__init__(name, price, category, year, "Magazine",
                         num_page=num_page)


class DVD(Item):
    def __init__(self, name, price, category, year, duration, num_file):
        super().__init__(name, price, category, year, "DVD",
                         duration=duration, num_file=num_file)



