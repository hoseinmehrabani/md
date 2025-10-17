import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class DailyPlanner:
    def __init__(self, db_name='daily_planner.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT,
                time TEXT
            )
        ''')
        self.conn.commit()

    def add_task(self, task, time):
        self.cursor.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (task, time))
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("برنامه‌ریز روزانه")
        self.planner = DailyPlanner()

        self.label = tk.Label(master, text="برنامه‌ریز روزانه", font=("Arial", 16))
        self.label.pack(pady=10)

        self.task_entry = tk.Entry(master, width=30)
        self.task_entry.pack(pady=5)
        self.task_entry.insert(0, "فعالیت جدید")

        self.time_entry = tk.Entry(master, width=30)
        self.time_entry.pack(pady=5)
        self.time_entry.insert(0, "زمان (ساعت:دقیقه)")

        self.add_button = tk.Button(master, text="افزودن فعالیت", command=self.add_task)
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(master, text="مشاهده فعالیت‌ها", command=self.view_tasks)
        self.view_button.pack(pady=5)

        self.delete_button = tk.Button(master, text="حذف فعالیت", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        time = self.time_entry.get()
        if task and time:
            self.planner.add_task(task, time)
            messagebox.showinfo("موفقیت", "فعالیت با موفقیت افزوده شد.")
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("خطا", "لطفاً هر دو فیلد را پر کنید.")

    def view_tasks(self):
        tasks = self.planner.get_tasks()
        if not tasks:
            messagebox.showinfo("فعالیتی یافت نشد", "هیچ فعالیتی در پایگاه داده وجود ندارد.")
            return
        tasks_list = "\n".join([f"{id}. {task} - {time}" for id, task, time in tasks])
        messagebox.showinfo("فعالیت‌ها", tasks_list)

    def delete_task(self):
        task_id = simpledialog.askinteger("حذف فعالیت", "شماره فعالیت را وارد کنید:")
        if task_id:
            self.planner.delete_task(task_id)
            messagebox.showinfo("موفقیت", "فعالیت با موفقیت حذف شد.")
        else:
            messagebox.showwarning("خطا", "لطفاً یک شماره معتبر وارد کنید.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
