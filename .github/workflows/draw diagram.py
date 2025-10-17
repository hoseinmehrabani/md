import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_chart():
    try:
        work = float(entry_work.get())
        exercise = float(entry_exercise.get())
        sleep = float(entry_sleep.get())
        eating = float(entry_eating.get())

        categories = ['کار', 'ورزش', 'خواب', 'خوردن']
        values = [work, exercise, sleep, eating]

        # پاک کردن نمودار قبلی
        ax.clear()
        ax.bar(categories, values, color=['blue', 'green', 'orange', 'red'])
        ax.set_xlabel('دسته‌بندی‌ها')
        ax.set_ylabel('ساعت')
        ax.set_title('نمودار زمان فعالیت‌ها')

        # بروزرسانی Canvas
        canvas.draw()
    except ValueError:
        messagebox.showerror("خطا", "لطفاً فقط اعداد وارد کنید.")

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("نمودار زمان فعالیت‌ها")

# ایجاد لیبل و ورودی برای هر پارامتر
labels = ['کار', 'ورزش', 'خواب', 'خوردن']
entries = {}

for label in labels:
    frame = tk.Frame(root)
    frame.pack(pady=5)
    lbl = tk.Label(frame, text=label)
    lbl.pack(side=tk.LEFT)
    entry = tk.Entry(frame)
    entry.pack(side=tk.RIGHT)
    entries[label] = entry

entry_work = entries['کار']
entry_exercise = entries['ورزش']
entry_sleep = entries['خواب']
entry_eating = entries['خوردن']

# ایجاد دکمه برای رسم نمودار
btn_draw = tk.Button(root, text="رسم نمودار", command=draw_chart)
btn_draw.pack(pady=20)

# ایجاد یک فریم برای نمودار
frame_chart = tk.Frame(root)
frame_chart.pack()

# ایجاد یک Figure و Axes برای رسم نمودار
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=frame_chart)
canvas.get_tk_widget().pack()

# شروع حلقه اصلی
root.mainloop()
