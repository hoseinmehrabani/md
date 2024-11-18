import tkinter as tk  
import random  

# تابعی برای پخش کردن دکمه‌ها  
def place_buttons_randomly(buttons, rows=4, columns=4):  
    # ایجاد یک آرایه از تمام موقعیت‌ها  
    positions = [(r, c) for r in range(1, rows) for c in range(columns)]  
    random.shuffle(positions)  # مخلوط کردن موقعیت‌ها  

    # قرار دادن دکمه‌ها در موقعیت‌های تصادفی  
    for button, (r, c) in zip(buttons, positions):  
        button.grid(row=r, column=c)  

window = tk.Tk()  
window.title("Calculator")  

# ایجاد دکمه‌ها  
buttons = [  
    tk.Button(window, text="1", padx=20, pady=10),  
    tk.Button(window, text="2", padx=20, pady=10),  
    tk.Button(window, text="3", padx=20, pady=10),  
    tk.Button(window, text="4", padx=20, pady=10),  
    tk.Button(window, text="5", padx=20, pady=10),  
    tk.Button(window, text="6", padx=20, pady=10),  
    tk.Button(window, text="7", padx=20, pady=10),  
    tk.Button(window, text="8", padx=20, pady=10),  
    tk.Button(window, text="9", padx=20, pady=10),  
    tk.Button(window, text="0", padx=20, pady=10),  
    tk.Button(window, text="#", padx=19, pady=10),  
    tk.Button(window, text="*", padx=21, pady=10),  
]  

window.configure(bg='yellow')  

# پخش کردن دکمه‌ها به صورت تصادفی  
place_buttons_randomly(buttons)  

window.mainloop()