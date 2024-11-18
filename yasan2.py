import tkinter as tk  
from tkinter import messagebox  # وارد کردن ماژول messagebox  

def get_text():  
    try:  
        # گرفتن متن از تکست باکس و تبدیل آن به عدد صحیح  
        number = int(text_box.get("1.0", tk.END).strip())  # تبدیل به عدد صحیح  
        van = number // 10  
        n = number % 10  
        if n > 0:  
            van += 1  
        hazine_van = van * 150000 // number  
        
        # نمایش نتیجه در یک پیام باکس  
        messagebox.showinfo("نتیجه", f"هزینه هر نفر: {hazine_van} تومان")  
        
    except ValueError:  
        messagebox.showerror("خطا", "لطفاً یک عدد صحیح وارد کنید!")  

# ایجاد پنجره اصلی  
root = tk.Tk()  
root.title("Text Box Example")  

lbl = tk.Label(root, text="تعداد دانش آموزان")  
lbl.pack()  

# ایجاد یک Textbox  
text_box = tk.Text(root, height=1, width=15)  
text_box.pack()  

# ایجاد دکمه برای گرفتن متن  
get_button = tk.Button(root, text="Get Text", command=get_text)  
get_button.pack(pady=10)  

# اجرای برنامه  
root.mainloop()