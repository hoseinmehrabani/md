import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import torch  # برای مدل YOLOv5
import matplotlib.pyplot as plt  # برای نمایش تصاویر

def preprocess_frame(frame):
    # تبدیل به خاکستری
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # انجام عملیات پردازش تصویر (مثلاً بلور کردن)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

def show_image(image, title=''):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def detect_sperms(model, video_path):
    total_sperms = 0
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        messagebox.showerror("خطا", "عدم توانایی بارگذاری ویدیو.")
        return

    while True:
        ret, frame = video.read()
        if not ret:
            break  # اگر فریم قابل خواندن نیست، حلقه را متوقف کن

        # پیش پردازش فریم
        processed_frame = preprocess_frame(frame)

        # تبدیل فریم به قالب مناسب برای مدل
        results = model(processed_frame)  # شناسایی اشیاء در فریم

        # پردازش نتایج
        for *box, conf, cls in results.xyxy[0]:  # نتایج مدل
            if conf > 0.1 and int(cls) == 0:  # آستانه اطمینان 0.1
                total_sperms += 1

        # نمایش فریم و تعداد اسپرم‌ها
        cv2.putText(frame, f"Sperms: {total_sperms}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        show_image(frame, "Frame with Detected Sperms")

    video.release()
    return total_sperms

def main():
    root = tk.Tk()
    root.withdraw()

    video_path = filedialog.askopenfilename(title="انتخاب فایل ویدیو", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if not video_path:
        return

    # بارگذاری مدل YOLOv5
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # بارگذاری مدل از پیش آموزش دیده

    # شناسایی اسپرم‌ها
    total_sperms = detect_sperms(model, video_path)

    # نمایش تعداد اسپرم‌های شناسایی شده
    messagebox.showinfo("نتیجه", f"تعداد اسپرم‌های زنده: {total_sperms}")

if __name__ == "__main__":
    main()
