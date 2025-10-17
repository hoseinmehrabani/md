import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

class MentalExercisesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("تمرینات ذهنی")

        self.exercises = [
            {"question": "چند تا عدد را به خاطر بسپارید: 5، 12، 23، 8، 34\n\nبعداً چند سوال در مورد این اعداد می‌پرسیم.", "answer": "5, 12, 23, 8, 34"},
            {"question": "چه رنگی را برای شماره 2 انتخاب می‌کنید؟\n\nیادداشت کنید و بعداً جواب دهید.", "answer": "قرمز"},
            {"question": "کلمه‌ی 'گربه' را برعکس کنید:", "answer": "تبرگ"},
            {"question": "ساده‌ترین عدد اول را بگویید:", "answer": "2"},
            {"question": "این سوال را جواب بدهید: 10 + 5 = ?", "answer": "15"},
            {"question": "عدد بعدی در دنباله 1، 1، 2، 3، 5 چیست؟", "answer": "8"},
            {"question": "پایتون یک زبان برنامه‌نویسی است. درست یا نادرست؟", "answer": "درست"},
            {"question": "عدد 100 را به 10 تقسیم کنید:", "answer": "10"},
        ]

        self.score = 0

        self.start_button = tk.Button(root, text="شروع تمرینات", command=self.start_exercise)
        self.start_button.pack(pady=20)

        self.exit_button = tk.Button(root, text="خروج", command=root.quit)
        self.exit_button.pack(pady=20)

    def start_exercise(self):
        exercise = random.choice(self.exercises)
        self.current_answer = exercise["answer"]
        self.time_limit = 10  # زمان محدود به ثانیه
        self.display_question(exercise["question"])
        self.start_timer()

    def display_question(self, question):
        self.question_window = tk.Toplevel(self.root)
        self.question_window.title("تمرین جدید")

        label = tk.Label(self.question_window, text=question, wraplength=300)
        label.pack(pady=10)

        self.timer_label = tk.Label(self.question_window, text=f"زمان باقی‌مانده: {self.time_limit} ثانیه")
        self.timer_label.pack(pady=10)

        answer_button = tk.Button(self.question_window, text="جواب دادم", command=self.check_answer)
        answer_button.pack(pady=10)

        self.answer_entry = tk.Entry(self.question_window)
        self.answer_entry.pack(pady=10)

    def start_timer(self):
        def countdown():
            while self.time_limit > 0:
                time.sleep(1)
                self.time_limit -= 1
                self.timer_label.config(text=f"زمان باقی‌مانده: {self.time_limit} ثانیه")
            if self.time_limit == 0:
                self.check_answer(timeout=True)

        threading.Thread(target=countdown).start()

    def check_answer(self, timeout=False):
        if timeout:
            messagebox.showwarning("زمان تمام شد!", "جواب ندادید!")
            self.current_answer = None  # Reset answer to show nothing on timeout
        else:
            user_answer = self.answer_entry.get().strip()
            if user_answer.lower() == self.current_answer.lower():
                messagebox.showinfo("موفقیت", "جواب درست است!")
                self.score += 1  # افزایش امتیاز
            else:
                messagebox.showwarning("خطا", f"جواب نادرست است! جواب صحیح: {self.current_answer}")
        self.question_window.destroy()
        self.show_score()

    def show_score(self):
        messagebox.showinfo("امتیاز", f"امتیاز شما: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalExercisesApp(root)
    root.mainloop()
