import tkinter as tk
from tkinter import messagebox
import sqlite3

class TravelGuide:
    def __init__(self, db_name='travel_guide.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attractions (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT,
                cuisine TEXT,
                description TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tips (
                id INTEGER PRIMARY KEY,
                content TEXT
            )
        ''')
        self.conn.commit()

    def add_attraction(self, name, description):
        self.cursor.execute("INSERT INTO attractions (name, description) VALUES (?, ?)", (name, description))
        self.conn.commit()

    def add_restaurant(self, name, cuisine, description):
        self.cursor.execute("INSERT INTO restaurants (name, cuisine, description) VALUES (?, ?, ?)", (name, cuisine, description))
        self.conn.commit()

    def add_tip(self, content):
        self.cursor.execute("INSERT INTO tips (content) VALUES (?)", (content,))
        self.conn.commit()

    def get_attractions(self):
        self.cursor.execute("SELECT * FROM attractions")
        return self.cursor.fetchall()

    def get_restaurants(self):
        self.cursor.execute("SELECT * FROM restaurants")
        return self.cursor.fetchall()

    def get_tips(self):
        self.cursor.execute("SELECT * FROM tips")
        return self.cursor.fetchall()

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("راهنمای سفر")
        self.guide = TravelGuide()

        self.label = tk.Label(master, text="به راهنمای سفر خوش آمدید!", font=("Arial", 16))
        self.label.pack(pady=10)

        self.attractions_button = tk.Button(master, text="جاذبه‌های گردشگری", command=self.show_attractions)
        self.attractions_button.pack(pady=5)

        self.restaurants_button = tk.Button(master, text="رستوران‌ها", command=self.show_restaurants)
        self.restaurants_button.pack(pady=5)

        self.tips_button = tk.Button(master, text="نکات سفر", command=self.show_tips)
        self.tips_button.pack(pady=5)

    def show_attractions(self):
        attractions = self.guide.get_attractions()
        if not attractions:
            messagebox.showinfo("جاذبه‌ای یافت نشد", "هیچ جاذبه‌ای در پایگاه داده وجود ندارد.")
            return
        info = "\n".join([f"{name}: {description}" for id, name, description in attractions])
        messagebox.showinfo("جاذبه‌های گردشگری", info)

    def show_restaurants(self):
        restaurants = self.guide.get_restaurants()
        if not restaurants:
            messagebox.showinfo("رستورانی یافت نشد", "هیچ رستورانی در پایگاه داده وجود ندارد.")
            return
        info = "\n".join([f"{name} ({cuisine}): {description}" for id, name, cuisine, description in restaurants])
        messagebox.showinfo("رستوران‌ها", info)

    def show_tips(self):
        tips = self.guide.get_tips()
        if not tips:
            messagebox.showinfo("نکاتی یافت نشد", "هیچ نکته‌ای در پایگاه داده وجود ندارد.")
            return
        info = "\n".join([content for id, content in tips])
        messagebox.showinfo("نکات سفر", info)

def create_database():
    conn = sqlite3.connect('travel_guide.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cuisine TEXT,
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY,
            content TEXT
        )
    ''')

    # افزودن اطلاعات اولیه
    cursor.execute("INSERT INTO attractions (name, description) VALUES ('برج ایفل', 'برج مشهور در پاریس')")
    cursor.execute("INSERT INTO attractions (name, description) VALUES ('کولوسئوم', 'تاریخی‌ترین آمفی‌تئاتر روم')")
    cursor.execute("INSERT INTO restaurants (name, cuisine, description) VALUES ('رستوران لا کاسا', 'فرانسوی', 'رستورانی با غذاهای خوشمزه فرانسوی')")
    cursor.execute("INSERT INTO restaurants (name, cuisine, description) VALUES ('رستوران گلابی', 'ایرانی', 'غذاهای سنتی ایرانی با کیفیت بالا')")
    cursor.execute("INSERT INTO tips (content) VALUES ('برای سفرهای خارجی ویزا را از قبل بگیرید.')")
    cursor.execute("INSERT INTO tips (content) VALUES ('سعی کنید زبان محلی را یاد بگیرید.')")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()  # ایجاد پایگاه داده و پر کردن آن
    root = tk.Tk()
    app = App(root)
    root.mainloop()
