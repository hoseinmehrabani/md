import tkinter as tk
from tkcalendar import Calendar
from persiantools.jdatetime import JalaliDate
from hijri_converter import convert

class CalendarApp:
    def __init__(self, master):
        self.master = master
        master.title("تقویم شمسی، میلادی و قمری")

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        # تقویم میلادی
        self.cal_gregorian = Calendar(self.frame, selectmode='day', year=2024, month=10, day=6,
                                       foreground='black', background='lightblue',
                                       headerbackground='darkblue', headerforeground='white',
                                       showweeknumbers=False)
        self.cal_gregorian.pack(padx=10, pady=10)
        self.label_gregorian = tk.Label(master, text="تقویم میلادی", font=('Arial', 14))
        self.label_gregorian.pack(pady=5)

        # تقویم شمسی
        self.cal_jalali = Calendar(self.frame, selectmode='day', year=1403, month=7, day=15,
                                    foreground='black', background='lightgreen',
                                    headerbackground='darkgreen', headerforeground='white',
                                    showweeknumbers=False)
        self.cal_jalali.pack(padx=10, pady=10)
        self.label_jalali = tk.Label(master, text="تقویم شمسی", font=('Arial', 14))
        self.label_jalali.pack(pady=5)

        # تقویم قمری
        self.cal_hijri = Calendar(self.frame, selectmode='day', year=1446, month=2, day=25,
                                  foreground='black', background='lightyellow',
                                  headerbackground='darkorange', headerforeground='white',
                                  showweeknumbers=False)
        self.cal_hijri.pack(padx=10, pady=10)
        self.label_hijri = tk.Label(master, text="تقویم قمری", font=('Arial', 14))
        self.label_hijri.pack(pady=5)

        self.result_label = tk.Label(master, text="", font=('Arial', 16))
        self.result_label.pack(pady=20)

        self.button = tk.Button(master, text="نمایش تاریخ انتخاب شده", command=self.show_date,
                                bg='blue', fg='white', font=('Arial', 12))
        self.button.pack(pady=10)

    def show_date(self):
        # تاریخ میلادی
        selected_date_gregorian = self.cal_gregorian.get_date()

        # تاریخ شمسی
        selected_date_jalali = self.cal_jalali.get_date()

        # تاریخ قمری
        selected_date_hijri = self.cal_hijri.get_date()

        # تبدیل تاریخ شمسی به میلادی
        year, month, day = map(int, selected_date_jalali.split('/'))
        jalali_date = JalaliDate(year, month, day)
        gregorian_from_jalali = jalali_date.to_gregorian().strftime('%Y/%m/%d')

        # تبدیل تاریخ قمری به شمسی و میلادی
        year, month, day = map(int, selected_date_hijri.split('/'))
        hijri_date = convert.Hijri(year, month, day)
        gregorian_from_hijri = hijri_date.to_gregorian()
        jalali_from_hijri = hijri_date.to_jalali()

        # نام ماه‌های شمسی
        jalali_month_names = [
            "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]

        # نام ماه‌های قمری
        hijri_month_names = [
            "محرم", "صفر", "ربیع‌الاول", "ربیع‌الثانی", "جمادی‌الاول",
            "جمادی‌الثانی", "رجب", "شعبان", "رمضان", "شوال",
            "ذوالقعده", "ذوالحجه"
        ]

        # نمایش تاریخ‌ها با نام ماه‌ها
        self.result_label.config(text=(
            f"تاریخ میلادی: {selected_date_gregorian}\n"
            f"تاریخ شمسی: {jalali_date.day} {jalali_month_names[jalali_date.month - 1]} {jalali_date.year}\n"
            f"تاریخ قمری: {hijri_date.day} {hijri_month_names[hijri_date.month - 1]} {hijri_date.year}\n"
            f"تاریخ میلادی از شمسی: {gregorian_from_jalali}\n"
            f"تاریخ شمسی از قمری: {jalali_from_hijri.day} {jalali_month_names[jalali_from_hijri.month - 1]} {jalali_from_hijri.year}\n"
            f"تاریخ میلادی از قمری: {gregorian_from_hijri.strftime('%Y/%m/%d')}"
        ))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.geometry("450x600")
    root.mainloop()
