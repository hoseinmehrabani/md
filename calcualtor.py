import tkinter as tk
import math
from tkinter import colorchooser


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("ماشین حساب پیشرفته")

        self.result = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.result, font=('Arial', 24), bd=10, insertwidth=4, width=14,
                              borderwidth=4)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.button_color = "#4CAF50"  # رنگ پیش‌فرض دکمه‌ها
        self.create_buttons()
        self.create_menu()

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        color_menu = tk.Menu(menu)
        menu.add_cascade(label="تنظیمات", menu=color_menu)
        color_menu.add_command(label="انتخاب رنگ پس‌زمینه", command=self.change_background)
        color_menu.add_command(label="انتخاب رنگ دکمه‌ها", command=self.change_button_color)

    def change_background(self):
        color_code = colorchooser.askcolor(title="انتخاب رنگ پس‌زمینه")
        if color_code[1]:  # اگر کاربر رنگی انتخاب کرده باشد
            self.master.config(bg=color_code[1])
            self.entry.config(bg=color_code[1])

    def change_button_color(self):
        color_code = colorchooser.askcolor(title="انتخاب رنگ دکمه‌ها")
        if color_code[1]:  # اگر کاربر رنگی انتخاب کرده باشد
            self.button_color = color_code[1]
            self.update_button_colors()

    def update_button_colors(self):
        for widget in self.master.grid_slaves():
            if isinstance(widget, tk.Button):
                widget.config(bg=self.button_color)

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            '%', 'log', 'ln',
            'sin', 'cos', 'tan', 'sqrt',
            '1/x', 'C', 'Clear'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            color = self.button_color if button not in ['=', 'C', 'Clear'] else "#f44336"  # رنگ دکمه‌ها
            btn = tk.Button(self.master, text=button, padx=20, pady=20, font=('Arial', 18),
                            bg=color, fg="white", activebackground="#45a049",
                            command=lambda b=button: self.on_button_click(b))
            btn.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nsew")
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # تنظیم نسبت ابعاد دکمه‌ها
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)
        for j in range(6):
            self.master.grid_rowconfigure(j, weight=1)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = str(eval(self.result.get()))
                self.result.set(result)
            except Exception:
                self.result.set("خطا")
        elif char in ['C', 'Clear']:
            self.clear()
        elif char == '%':
            try:
                value = float(self.result.get())
                self.result.set(value / 100)
            except ValueError:
                self.result.set("خطا")
        elif char == 'log':
            try:
                value = float(self.result.get())
                self.result.set(math.log10(value))  # لگاریتم بر مبنای 10
            except ValueError:
                self.result.set("خطا")
        elif char == 'ln':
            try:
                value = float(self.result.get())
                self.result.set(math.log(value))  # لگاریتم طبیعی
            except ValueError:
                self.result.set("خطا")
        elif char == 'sin':
            try:
                value = math.radians(float(self.result.get()))  # تبدیل به رادیان
                self.result.set(math.sin(value))
            except ValueError:
                self.result.set("خطا")
        elif char == 'cos':
            try:
                value = math.radians(float(self.result.get()))
                self.result.set(math.cos(value))
            except ValueError:
                self.result.set("خطا")
        elif char == 'tan':
            try:
                value = math.radians(float(self.result.get()))
                self.result.set(math.tan(value))
            except ValueError:
                self.result.set("خطا")
        elif char == 'sqrt':
            try:
                value = float(self.result.get())
                self.result.set(math.sqrt(value))  # ریشه دوم
            except ValueError:
                self.result.set("خطا")
        elif char == '1/x':
            try:
                value = float(self.result.get())
                self.result.set(1 / value)  # معکوس
            except ValueError:
                self.result.set("خطا")
        else:
            current = self.result.get()
            self.result.set(current + char)

    def clear(self):
        self.result.set("")


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.geometry("400x600")
    root.mainloop()
