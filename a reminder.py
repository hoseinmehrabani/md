import tkinter as tk
from tkinter import messagebox
import schedule
import time
import threading


class HealthReminder:
    def __init__(self):
        self.reminders = {
            'water': 'وقت نوشیدن آب است!',
            'exercise': 'وقت ورزش کردن است!',
            'medication': 'وقت مصرف دارو است!'
        }

    def start_reminders(self):
        schedule.every().hour.at(":00").do(self.remind, 'water')
        schedule.every().hour.at(":30").do(self.remind, 'exercise')
        schedule.every().day.at("08:00").do(self.remind, 'medication')

        while True:
            schedule.run_pending()
            time.sleep(1)

    def remind(self, reminder_type):
        messagebox.showinfo("یادآور سلامت", self.reminders[reminder_type])


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("یادآور سلامت")
        self.reminder = HealthReminder()

        self.label = tk.Label(master, text="یادآور سلامت", font=("Arial", 16))
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="شروع یادآوری‌ها", command=self.start_reminders)
        self.start_button.pack(pady=5)

    def start_reminders(self):
        threading.Thread(target=self.reminder.start_reminders, daemon=True).start()
        messagebox.showinfo("یادآوری", "یادآوری‌ها شروع شدند!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
