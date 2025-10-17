import requests
import tkinter as tk
from tkinter import messagebox

# کلید API خود را اینجا قرار دهید
API_KEY = "YOUR_API_KEY"  # کلید API را اینجا قرار دهید


# تابعی برای دریافت نقل‌قول از API
def get_quote():
    url = "https://quotes.rest/qod?category=inspire"  # API برای نقل‌قول‌های انگیزشی
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        quote = data['contents']['quotes'][0]['quote']
        author = data['contents']['quotes'][0]['author']
        return f"{quote}\n\n- {author}"
    else:
        return "خطا در دریافت نقل‌قول."


# تابعی برای نمایش نقل‌قول
def show_quote():
    quote = get_quote()
    messagebox.showinfo("نقل‌قول روز", quote)


# ساخت رابط کاربری
def create_gui():
    root = tk.Tk()
    root.title("نقل‌قول‌های روزانه")

    label = tk.Label(root, text="برای دریافت نقل‌قول روز بر روی دکمه زیر کلیک کنید:")
    label.pack(pady=20)

    button = tk.Button(root, text="نقل‌قول جدید", command=show_quote)
    button.pack(pady=10)

    exit_button = tk.Button(root, text="خروج", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
