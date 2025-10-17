import cv2
import tkinter as tk 
from PIL import ImageTk, Image
# مسیر فایل تصویر png را تعیین کنید 
image_path = "2829479_preview.jpg" 
# باز کردن تصویر با استفاده از 
#OpenCV 
image = cv2.imread(image_path) 
# تبدیل فرمت تصویر از BGR به RGB 
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
# تبدیل تصویر به شی 
#PIL.Image 
image = Image.fromarray(image) 
# ساخت یک پنجره تک پنجره تک پنجره تک تک پنجره تک 30 ماهه 
window = tk.Tk() 
# ساخت یک برچسب برای نمایش تصویر 
label = tk.Label(window) 
# نمایش تصویر در برچسب 
label.image = ImageTk.PhotoImage(image) 
label.config(image=label.image) 
label.pack() 
# نمایش پنجره 
window.mainloop()