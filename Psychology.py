import tkinter as tk
from tkinter import messagebox
import sqlite3


class PersonalityTest:
    def __init__(self, db_name='personality_tests.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.load_tests()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY,
                title TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                test_id INTEGER,
                question TEXT,
                option1 TEXT,
                option2 TEXT,
                FOREIGN KEY(test_id) REFERENCES tests(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                test_id INTEGER,
                introvert TEXT,
                extrovert TEXT,
                FOREIGN KEY(test_id) REFERENCES tests(id)
            )
        ''')
        self.conn.commit()

    def load_tests(self):
        self.cursor.execute("SELECT * FROM tests")
        self.tests = self.cursor.fetchall()

    def get_tests(self):
        return self.tests

    def get_questions(self, test_id):
        self.cursor.execute("SELECT * FROM questions WHERE test_id=?", (test_id,))
        return self.cursor.fetchall()

    def get_results(self, test_id):
        self.cursor.execute("SELECT * FROM results WHERE test_id=?", (test_id,))
        return self.cursor.fetchone()


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("تست‌های روانشناسی و شخصیت")
        self.test_manager = PersonalityTest()

        self.label = tk.Label(master, text="به برنامه تست شخصیت خوش آمدید!", font=("Arial", 16))
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="شروع تست", command=self.start_test)
        self.start_button.pack(pady=5)

        self.test_results = None

    def start_test(self):
        tests = self.test_manager.get_tests()
        if not tests:
            messagebox.showwarning("خطا", "تست‌هایی برای نمایش وجود ندارد.")
            return

        test_id = tests[0][0]  # برای سادگی، فقط اولین تست را انتخاب می‌کنیم
        self.test_results = []

        self.test_window = tk.Toplevel(self.master)
        self.test_window.title(tests[0][1])

        self.question_label = tk.Label(self.test_window, text="")
        self.question_label.pack(pady=10)

        self.var = tk.StringVar()

        self.option_buttons = []
        for i in range(2):
            button = tk.Radiobutton(self.test_window, text="", variable=self.var, value=i)
            button.pack(anchor='w')
            self.option_buttons.append(button)

        self.next_button = tk.Button(self.test_window, text="سوال بعدی", command=lambda: self.next_question(test_id))
        self.next_button.pack(pady=10)

        self.current_question = 0
        self.questions = self.test_manager.get_questions(test_id)
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data[2])
            self.option_buttons[0].config(text=question_data[3])
            self.option_buttons[1].config(text=question_data[4])
        else:
            self.show_results()

    def next_question(self, test_id):
        selected_value = self.var.get()
        if selected_value == "":
            messagebox.showwarning("خطا", "لطفا یک گزینه را انتخاب کنید.")
            return

        self.test_results.append(int(selected_value))
        self.current_question += 1
        self.show_question()

    def show_results(self):
        self.test_window.destroy()

        score = sum(self.test_results)
        result_data = self.test_manager.get_results(1)  # با فرض اینکه فقط یک تست داریم
        result_key = 'introvert' if score < len(self.questions) / 2 else 'extrovert'
        result_message = result_data[2] if result_key == 'introvert' else result_data[3]

        messagebox.showinfo("نتایج تست", result_message)


def create_database():
    conn = sqlite3.connect('personality_tests.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY,
            title TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            test_id INTEGER,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            FOREIGN KEY(test_id) REFERENCES tests(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            test_id INTEGER,
            introvert TEXT,
            extrovert TEXT,
            FOREIGN KEY(test_id) REFERENCES tests(id)
        )
    ''')

    cursor.execute("INSERT INTO tests (title) VALUES ('تست شخصیت آیزنک')")
    cursor.execute(
        "INSERT INTO questions (test_id, question, option1, option2) VALUES (1, 'آیا شما فردی خجالتی هستید؟', 'بله', 'خیر')")
    cursor.execute(
        "INSERT INTO questions (test_id, question, option1, option2) VALUES (1, 'آیا دوست دارید در جمع‌های بزرگ باشید؟', 'بله', 'خیر')")
    cursor.execute(
        "INSERT INTO results (test_id, introvert, extrovert) VALUES (1, 'شما فردی درون‌گرا هستید.', 'شما فردی برون‌گرا هستید.' )")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()  # ایجاد پایگاه داده و پر کردن آن
    root = tk.Tk()
    app = App(root)
    root.mainloop()
