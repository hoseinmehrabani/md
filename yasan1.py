import tkinter as tk  
from tkinter import messagebox  # وارد کردن ماژول messagebox  

def get_text():  
    try:  
        # گرفتن متن از تکست باکس و تبدیل آن به عدد صحیح  
        s = int(text_box.get("1.0", tk.END).strip())  # تبدیل به عدد صحیح  
        g=0
        if s>=10:
            g=int(input("لطفا قد را وارد کنید :"))
        if g>140:
            messagebox.showinfo("شما مجاز به ثبت نام هستید")
        else:    
            if g>140:
            messagebox.showinfo("شما مجاز به ثبت نام هستید")
        else:    
           # نمایش نتیجه در یک پیام باکس  
            messagebox.showinfo('ERROR')  
        
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
