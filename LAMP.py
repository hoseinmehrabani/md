import tkinter as tk  
root = tk.Tk()  
x = 0
default_color = root.cget("bg")  # رنگ پس‌زمینه پیش‌فرض پنجره  
def fde():  
    global x  # استفاده از متغیر سراسری x  
    if x == 0:  
        lbl.config(background="yellow")  # تغییر پس‌زمینه به زرد  
        x = 1  # به حالت 1 تغییر حالت می‌دهیم  
    else:  
        lbl.config(background=default_color)  # بازگشت به رنگ پیش‌فرض  
        x = 0  # به حالت 0 بازمی‌گردیم  
lbl = tk.Label(root, text="چراغ")  
lbl.grid(row=0, column=1)  
btn1 = tk.Button(root, text="کلید", command=fde)  
btn1.grid(row=5, column=3)  
root.mainloop()