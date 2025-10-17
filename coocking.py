import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image
import os
import threading
import time

# ایجاد یا اتصال به دیتابیس
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# ایجاد جدول دستورپخت‌ها
cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    image TEXT,
    calories INTEGER
)
''')

# ایجاد جدول نظرات و امتیازها
cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    rating INTEGER,
    comment TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
)
''')
conn.commit()


def add_recipe(name, ingredients, instructions, image, calories):
    cursor.execute('INSERT INTO recipes (name, ingredients, instructions, image, calories) VALUES (?, ?, ?, ?, ?)',
                   (name, ingredients, instructions, image, calories))
    conn.commit()


def get_recipe(name):
    cursor.execute('SELECT * FROM recipes WHERE name = ?', (name,))
    return cursor.fetchone()


def get_all_recipes():
    cursor.execute('SELECT name FROM recipes')
    return cursor.fetchall()


def delete_recipe(recipe_id):
    cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()


def update_recipe(recipe_id, name, ingredients, instructions, image, calories):
    cursor.execute(
        'UPDATE recipes SET name = ?, ingredients = ?, instructions = ?, image = ?, calories = ? WHERE id = ?',
        (name, ingredients, instructions, image, calories, recipe_id))
    conn.commit()


def add_review(recipe_id, rating, comment):
    cursor.execute('INSERT INTO reviews (recipe_id, rating, comment) VALUES (?, ?, ?)',
                   (recipe_id, rating, comment))
    conn.commit()


def get_reviews(recipe_id):
    cursor.execute('SELECT rating, comment FROM reviews WHERE recipe_id = ?', (recipe_id,))
    return cursor.fetchall()


def show_recipe():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    recipe = get_recipe(recipe_name)
    if recipe:
        ingredients, instructions, image, calories = recipe[2], recipe[3], recipe[4], recipe[5]
        ingredients_text = f"مواد:\n{ingredients}\n\nدستور:\n{instructions}\n\nکالری: {calories} کیلوکالری"
        messagebox.showinfo(recipe_name, ingredients_text)
        if image and os.path.exists(image):
            img = Image.open(image)
            img.show()

        # نمایش نظرات
        reviews = get_reviews(recipe[0])
        if reviews:
            review_text = "\n".join([f"امتیاز: {r[0]}, نظر: {r[1]}" for r in reviews])
            messagebox.showinfo("نظرات", review_text)
        else:
            messagebox.showinfo("نظرات", "هیچ نظری وجود ندارد.")
    else:
        messagebox.showwarning("هشدار", "دستورپختی با این نام وجود ندارد.")


def add_recipe_ui():
    name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    ingredients = simpledialog.askstring("مواد", "مواد را وارد کنید (به فرمت: نام: مقدار; نام: مقدار):")
    instructions = simpledialog.askstring("دستور", "دستور پخت را وارد کنید:")
    image = simpledialog.askstring("عکس", "آدرس عکس را وارد کنید:")
    calories = simpledialog.askinteger("کالری", "کالری دستورپخت را وارد کنید:")
    if name and ingredients and instructions:
        add_recipe(name, ingredients, instructions, image, calories)
        messagebox.showinfo("موفقیت", "دستورپخت با موفقیت ذخیره شد.")


def delete_recipe_ui():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    recipe = get_recipe(recipe_name)
    if recipe:
        delete_recipe(recipe[0])
        messagebox.showinfo("موفقیت", "دستورپخت با موفقیت حذف شد.")
    else:
        messagebox.showwarning("هشدار", "دستورپختی با این نام وجود ندارد.")


def update_recipe_ui():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    recipe = get_recipe(recipe_name)
    if recipe:
        new_name = simpledialog.askstring("نام جدید", "نام جدید را وارد کنید:", initialvalue=recipe[1])
        ingredients = simpledialog.askstring("مواد", "مواد را وارد کنید:", initialvalue=recipe[2])
        instructions = simpledialog.askstring("دستور", "دستور پخت را وارد کنید:", initialvalue=recipe[3])
        image = simpledialog.askstring("عکس", "آدرس عکس را وارد کنید:", initialvalue=recipe[4])
        calories = simpledialog.askinteger("کالری", "کالری جدید را وارد کنید:", initialvalue=recipe[5])
        update_recipe(recipe[0], new_name, ingredients, instructions, image, calories)
        messagebox.showinfo("موفقیت", "دستورپخت با موفقیت ویرایش شد.")
    else:
        messagebox.showwarning("هشدار", "دستورپختی با این نام وجود ندارد.")


def convert_ingredients(ingredients, servings):
    ingredients_dict = {}
    for item in ingredients.split(';'):
        if ':' in item:
            ingredient, amount = item.split(':')
            ingredients_dict[ingredient.strip()] = float(amount.strip())
    converted_ingredients = {item: amount * servings / 4 for item, amount in ingredients_dict.items()}
    return converted_ingredients


def convert_ingredients_ui():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    servings = simpledialog.askinteger("تعداد نفرات", "تعداد نفرات را وارد کنید:", minvalue=1)
    recipe = get_recipe(recipe_name)
    if recipe:
        ingredients, _ = recipe[2], recipe[3]
        converted = convert_ingredients(ingredients, servings)
        ingredients_text = "\n".join([f"{item}: {amount:.2f} گرم" for item, amount in converted.items()])
        messagebox.showinfo("مقادیر تبدیل‌شده", f"برای {servings} نفر:\n{ingredients_text}")
    else:
        messagebox.showwarning("هشدار", "دستورپختی با این نام وجود ندارد.")


def list_shopping_list():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    recipe = get_recipe(recipe_name)
    if recipe:
        ingredients = recipe[2]
        shopping_list = "\n".join([item.strip() for item in ingredients.split(';')])
        messagebox.showinfo("لیست خرید", f"لیست خرید برای {recipe_name}:\n{shopping_list}")
    else:
        messagebox.showwarning("هشدار", "دستورپختی با این نام وجود ندارد.")


def add_review_ui():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    recipe = get_recipe(recipe_name)
    if recipe:
        rating = simpledialog.askinteger("امتیاز", "امتیاز (1 تا 5) را وارد کنید:", minvalue=1, maxvalue=5)
        comment = simpledialog.askstring("نظر", "نظر خود را وارد کنید:")
        add_review(recipe[0], rating, comment)
        messagebox.showinfo("موفقیت", "نظر با موفقیت اضافه شد.")
    else:
        messagebox.showwarning("هشدار", "دستورپختی با این نام وجود ندارد.")


def timer_reminder_ui():
    recipe_name = simpledialog.askstring("نام دستورپخت", "نام دستورپخت را وارد کنید:")
    cooking_time = simpledialog.askinteger("زمان پخت", "زمان پخت (به دقیقه) را وارد کنید:", minvalue=1)
    if recipe_name and cooking_time:
        messagebox.showinfo("یادآوری", f"یادآوری برای {recipe_name} تنظیم شد.")
        threading.Thread(target=timer_reminder, args=(cooking_time,)).start()


def timer_reminder(minutes):
    time.sleep(minutes * 60)
    messagebox.showinfo("یادآوری!", "زمان پخت تمام شده است!")


# ایجاد رابط کاربری
root = tk.Tk()
root.title("برنامه دستورپخت")

add_button = tk.Button(root, text="افزودن دستورپخت", command=add_recipe_ui)
add_button.pack(pady=10)

show_button = tk.Button(root, text="نمایش دستورپخت", command=show_recipe)
show_button.pack(pady=10)

delete_button = tk.Button(root, text="حذف دستورپخت", command=delete_recipe_ui)
delete_button.pack(pady=10)

update_button = tk.Button(root, text="ویرایش دستورپخت", command=update_recipe_ui)
update_button.pack(pady=10)

convert_button = tk.Button(root, text="تبدیل مقادیر", command=convert_ingredients_ui)
convert_button.pack(pady=10)

shopping_button = tk.Button(root, text="لیست خرید", command=list_shopping_list)
shopping_button.pack(pady=10)

review_button = tk.Button(root, text="اضافه کردن نظر", command=add_review_ui)
review_button.pack(pady=10)

timer_button = tk.Button(root, text="تنظیم یادآوری", command=timer_reminder_ui)
timer_button.pack(pady=10)

exit_button = tk.Button(root, text="خروج", command=root.quit)
exit_button.pack(pady=10)

root.mainloop()

# بستن اتصال به دیتابیس
conn.close()
