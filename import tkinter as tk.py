import tkinter as tk
def change_color(label):
    if label.cget('bg') == 'blue':
        label.config(bg='red')
    elif label.cget('bg') == 'red':
        label.config(bg='green')
    elif label.cget('bg')=='green':
        label.config(bg='yellow')
    else:
        label.config(bg='blue')
    label.after(2000, change_color, label)
# ایجاد پنجره
window = tk.Tk()
window.geometry('200x100')
# ایجاد دو لیبل با رنگ اولیه
label1 = tk.Label(window, text='اینجا', bg='red', fg='black')
label1.pack(fill=tk.BOTH, expand=tk.YES)

label2 = tk.Label(window, text='تراشه', bg='blue', fg='white')
label2.pack(fill=tk.BOTH, expand=tk.YES)

# فراخوانی تابع برای تغییر رنگها
change_color(label1)
change_color(label2)

# شروع حلقه‌ی رویدادها
window.mainloop()
