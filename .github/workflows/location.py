import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim

def get_location():
    geolocator = Nominatim(user_agent="my_unique_app_name")  # تغییر user_agent
    location = geolocator.geocode("iran")  # اینجا آدرس خود را وارد کنید
    if location:
        msg = f"Location: {location.latitude}, {location.longitude}"
    else:
        msg = "Location not found!"

    messagebox.showinfo("Location", msg)

# ایجاد رابط کاربری
root = tk.Tk()
root.title("Get Location")

# ایجاد دکمه
button = tk.Button(root, text="Get Location", command=get_location)
button.pack(pady=20)

# اجرای حلقه اصلی
root.mainloop()
