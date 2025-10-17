# وارد کردن کتابخانه Tkinter
from tkinter import *
# تعریف یک کلاس سفارشی که از کلاس Label ارث بری می‌کند
class ResizableLabel(Label):
    # تعریف یک متد برای ایجاد یک نمونه از این کلاس
    def __init__(self, master, text, font, **kwargs):
        # فراخوانی متد __init__ کلاس پدر
        super().__init__(master, text=text, font=font, **kwargs)
        # تعریف یک متغیر برای نگهداری مختصات ماوس
        self.x = 0
        self.y = 0
        # تعریف یک متغیر برای نگهداری وضعیت تغییر اندازه
        self.resizing = False
        # تعریف یک متغیر برای نگهداری شماره دسته‌ای که روی آن کلیک شده است
        self.handle = 0
        # تعریف یک متغیر برای نگهداری اندازه اولیه لیبل
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        # تعریف یک متغیر برای نگهداری اندازه حداقل لیبل
        self.min_width = self.width
        self.min_height = self.height
        # تعریف یک متغیر برای نگهداری اندازه حداکثر لیبل
        self.max_width = self.master.winfo_width()
        self.max_height = self.master.winfo_height()
        # تعریف یک متغیر برای نگهداری مقدار افزایش اندازه لیبل
        self.step = 10
        # تعریف یک متغیر برای نگهداری رنگ دسته‌ها
        self.handle_color = "blue"
        # تعریف یک متغیر برای نگهداری اندازه دسته‌ها
        self.handle_size = 0
        # تعریف یک متغیر برای نگهداری شکل دسته‌ها
        self.handle_shape = "oval"
        # تعریف یک متغیر برای نگهداری شناسه‌های دسته‌ها
        self.handles = []
        # ایجاد چهار دسته در گوشه‌های لیبل
        self.create_handles()
        # اتصال رویدادهای ماوس به توابع مربوطه
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    # تعریف یک متد برای ایجاد دسته‌ها
    def create_handles(self):
        # حذف دسته‌های قبلی اگر وجود داشته باشند
        for handle in self.handles:
            self.master.delete(handle)
        # خالی کردن لیست شناسه‌های دسته‌ها
        self.handles = []
        # محاسبه مختصات گوشه‌های لیبل
        x1 = self.winfo_x()
        y1 = self.winfo_y()
        x2 = x1 + self.width
        y2 = y1 + self.height
        # ایجاد دسته‌ها با استفاده از متد create_oval
        self.handles.append(self.master.create_oval(x1 - self.handle_size, y1 - self.handle_size, x1 + self.handle_size, y1 + self.handle_size, fill=self.handle_color))
        self.handles.append(self.master.create_oval(x2 - self.handle_size, y1 - self.handle_size, x2 + self.handle_size, y1 + self.handle_size, fill=self.handle_color))
        self.handles.append(self.master.create_oval(x1 - self.handle_size, y2 - self.handle_size, x1 + self.handle_size, y2 + self.handle_size, fill=self.handle_color))
        self.handles.append(self.master.create_oval(x2 - self.handle_size, y2 - self.handle_size, x2 + self.handle_size, y2 + self.handle_size, fill=self.handle_color))

    # تعریف یک متد برای ذخیره مختصات ماوس و شناسایی دسته‌ای که روی آن کلیک شده است
    def on_click(self, event):
        self.x = event.x
        self.y = event.y
        self.resizing = False
        self.handle = 0
        for i, handle in enumerate(self.handles):
            if self.master.find_withtag(CURRENT) == (handle,):
                self.resizing = True
                self.handle = i + 1
                break

    # تعریف یک متد برای جابجایی یا تغییر اندازه لیبل بر اساس دسته‌ای که روی آن کلیک شده است
    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        if self.resizing:
            if self.handle == 1:
                self.width -= dx
                self.height -= dy
                self.place(x=self.winfo_x() + dx, y=self.winfo_y() + dy)
            elif self.handle == 2:
                self.width += dx
                self.height -= dy
                self.place(y=self.winfo_y() + dy)
            elif self.handle == 3:
                self.width -= dx
                self.height += dy
                self.place(x=self.winfo_x() + dx)
            elif self.handle == 4:
                self.width += dx
                self.height += dy
            self.width = max(self.min_width, min(self.max_width, self.width))
            self.height = max(self.min_height, min(self.max_height, self.height))
            self.config(width=self.width, height=self.height)
            self.create_handles()
        else:
            self.place(x=self.winfo_x() + dx, y=self.winfo_y() + dy)
        self.x = event.x
        self.y = event.y

    # تعریف یک متد برای پایان دادن به تغییر اندازه
    def on_release(self, event):
        self.resizing = False
        self.handle = 0

# ساختن یک نمونه از کلاس Tk که نماینده پنجره اصلی است
root = Tk()

# ساختن یک نمونه از کلاس Canvas که نماینده یک صفحه برای رسم است
canvas = Canvas(root, width=1000, height=500)
canvas.pack()

# ساختن یک نمونه از کلاس Label که نماینده یک متن است
#label = Label(canvas, text="Hello World", font=("Arial", 10))
label = ResizableLabel(canvas, text="Hello World", font=("Arial", 20))
# قرار دادن لیبل در وسط صفحه با استفاده از متد create_window
canvas.create_window(200, 150, window=label)
# نمایش پنجره با استفاده از متد mainloop
root.mainloop()