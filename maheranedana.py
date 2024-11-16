import sqlite3  
import tkinter as tk  
from tkinter import messagebox  
import random  

# ایجاد یا اتصال به پایگاه داده SQLite  
conn = sqlite3.connect('knowledge_base.db')  
c = conn.cursor()  

# ایجاد جدول سوالات و پاسخ‌ها  
c.execute('''CREATE TABLE IF NOT EXISTS qa (question TEXT, answer TEXT)''')  
conn.commit()  

# تابع برای ذخیره سوال و جواب  
def save_qa():  
    question = question_entry.get()  
    answer = answer_entry.get()  
    
    if question and answer:  
        c.execute('INSERT INTO qa (question, answer) VALUES (?, ?)', (question, answer))  
        conn.commit()  
        messagebox.showinfo("موفقیت", "سوال و جواب ذخیره شد!")  
        question_entry.delete(0, tk.END)  
        answer_entry.delete(0, tk.END)  
    else:  
        messagebox.showwarning("خطای ورودی", "هر دو فیلد باید پر شوند!")  

# تابع برای جستجوی سوال  
def find_answer():  
    question = search_entry.get()  
    
    if question:  
        c.execute('SELECT answer FROM qa WHERE question = ?', (question,))  
        results = c.fetchall()  
        
        if results:  
            answer = random.choice(results)[0]  
            messagebox.showinfo("پاسخ پیدا شد", answer)  
        else:  
            messagebox.showinfo("یافت نشد", "هیچ پاسخی برای این سوال پیدا نشد.")  
    else:  
        messagebox.showwarning("خطای ورودی", "لطفاً یک سوال برای جستجو وارد کنید.")  

# ایجاد رابط کاربری  
root = tk.Tk()  
root.title("ربات یادگیری")  

# Textbox برای سوال  
question_entry = tk.Entry(root, width=50)  
question_entry.pack(pady=5)  
question_entry.insert(0, "سوال خود را اینجا وارد کنید...")  

# Textbox برای جواب  
answer_entry = tk.Entry(root, width=50)  
answer_entry.pack(pady=5)  
answer_entry.insert(0, "پاسخ را اینجا وارد کنید...")  

# دکمه برای ذخیره  
save_button = tk.Button(root, text="ذخیره سوال و جواب", command=save_qa)  
save_button.pack(pady=5)  

# Textbox برای جستجو  
search_entry = tk.Entry(root, width=50)  
search_entry.pack(pady=5)  
search_entry.insert(0, "سوال خود را برای جستجو وارد کنید...")  

# دکمه برای جستجو  
search_button = tk.Button(root, text="پیدا کردن پاسخ", command=find_answer)  
search_button.pack(pady=5)  

# اجرای رابط کاربری  
root.mainloop()  

# بستن پایگاه داده هنگام خروج  
conn.close()
