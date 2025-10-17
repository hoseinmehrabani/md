from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Start a new instance of the Chrome WebDriver
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://www.example.com")

# Locate the element that performs the action you want to skip or reject
element_to_skip = driver.find_element_by_id("element_id")  # Change 'element_id' to the actual ID of the element

# Simulate pressing the Enter key on the element to skip/reject the step
element_to_skip.send_keys(Keys.RETURN)

# Continue with the rest of your code here

# Close the browser session
driver.quit()
# وارد کردن کتابخانه Tkinter
"""from tkinter import *

# تعریف یک تابع پاسخگو برای رویداد فشار دادن کلید Enter
def show_text(event):
    # گرفتن متن وارد شده در ورودی
    text = entry.get()
    # چاپ کردن متن در برچسب
    label.config(text=text)

# ساختن یک نمونه از کلاس Tk که نماینده پنجره اصلی است
root = Tk()

# ساختن یک نمونه از کلاس Entry که نماینده یک ورودی است
entry = Entry(root)
entry.pack()

# ساختن یک نمونه از کلاس Label که نماینده یک برچسب است
label = Label(root, text="Enter some text and press Enter")
label.pack()

# اتصال رویداد فشار دادن کلید Enter به تابع پاسخگو با استفاده از متد bind
entry.bind("<Return>", show_text)

# نمایش پنجره با استفاده از متد mainloop
root.mainloop()"""
