import requests
from bs4 import BeautifulSoup
import random
import tkinter as tk
from tkinter import messagebox

# تابع برای استخراج اشعار حافظ
def get_hafez_ghazals():
    url = "https://www.bonbast.com/hafez/"
    response = requests.get(url)

    if response.status_code != 200:
        print("خطا در بارگذاری صفحه")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    ghazals = []

    # استخراج اشعار از div های دارای کلاس خاص
    for div in soup.find_all("div", class_="ghazal"):
        poem = div.get_text(separator="\n").strip()
        if poem:  # اطمینان از این که شعر خالی نیست
            ghazals.append(poem)

    return ghazals

# تابع برای استخراج تفسیر
def get_meaning(poem):
    return f"تفسیر شعر: این شعر درباره عشق و زندگی است."

# تابع برای گرفتن فال
def get_fal():
    ghazals = get_hafez_ghazals()
    if not ghazals:
        messagebox.showerror("خطا", "اشعار یافت نشد.")
        return

    fal = random.choice(ghazals)
    meaning = get_meaning(fal)

    result_text.delete(1.0, tk.END)  # پاک کردن متن قبلی
    result_text.insert(tk.END, f"فال شما:\n{fal}\n\nتفسیر:\n{meaning}")

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("فال حافظ")

# ایجاد دکمه برای گرفتن فال
get_fal_button = tk.Button(root, text="گرفتن فال حافظ", command=get_fal, padx=20, pady=10)
get_fal_button.pack(pady=20)

# ایجاد کادر متنی برای نمایش نتیجه
result_text = tk.Text(root, wrap=tk.WORD, width=60, height=20, font=("B Nazanin", 12))
result_text.pack(padx=10, pady=10)

# اجرای حلقه اصلی Tkinter
root.mainloop()
#
# import requests
# from bs4 import BeautifulSoup
# import random
# import tkinter as tk
# from tkinter import messagebox
#
#
# # تابع برای استخراج اشعار و تفسیرها
# def get_hafez_ghazals_and_meanings():
#     url = "https://www.bonbast.com/hafez/"
#     response = requests.get(url)
#
#     if response.status_code != 200:
#         print("خطا در بارگذاری صفحه")
#         return []
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#     ghazals = []
#
#     # استخراج اشعار و تفسیرها
#     for div in soup.find_all("div", class_="ghazal"):
#         poem = div.get_text(separator="\n").strip()
#         meaning_div = div.find_next("div", class_="ghazal-meaning")  # فرض بر این است که تفسیر در div جداگانه است
#         meaning = meaning_div.get_text(separator="\n").strip() if meaning_div else "تفسیر موجود نیست."
#
#         if poem:  # اطمینان از این که شعر خالی نیست
#             ghazals.append((poem, meaning))
#
#     return ghazals
#
#
# # تابع برای گرفتن فال
# def get_fal():
#     ghazals = get_hafez_ghazals_and_meanings()
#     if not ghazals:
#         messagebox.showerror("خطا", "اشعار یافت نشد.")
#         return
#
#     fal, meaning = random.choice(ghazals)
#
#     result_text.delete(1.0, tk.END)  # پاک کردن متن قبلی
#     result_text.insert(tk.END, f"فال شما:\n{fal}\n\nتفسیر:\n{meaning}")
#
#
# # ایجاد پنجره اصلی
# root = tk.Tk()
# root.title("فال حافظ")
#
# # ایجاد دکمه برای گرفتن فال
# get_fal_button = tk.Button(root, text="گرفتن فال حافظ", command=get_fal, padx=20, pady=10)
# get_fal_button.pack(pady=20)
#
# # ایجاد کادر متنی برای نمایش نتیجه
# result_text = tk.Text(root, wrap=tk.WORD, width=60, height=20, font=("B Nazanin", 12))
# result_text.pack(padx=10, pady=10)
#
# # اجرای حلقه اصلی Tkinter
# root.mainloop()
