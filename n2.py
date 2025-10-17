import cv2  
import tkinter as tk  
from tkinter import filedialog, messagebox  
import torch  
import matplotlib.pyplot as plt  
import numpy as np  

def preprocess_frame(frame):  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  
    return gray  

def show_image(image, title=''):  
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  
    plt.title(title)  
    plt.axis('off')  
    plt.show()  

def detect_moving_sperms(model, video_path):  
    total_moving_sperms = 0  
    previous_frame = None  
    video = cv2.VideoCapture(video_path)  

    if not video.isOpened():  
        messagebox.showerror("خطا", "عدم توانایی بارگذاری ویدیو.")  
        return  

    while True:  
        ret, frame = video.read()  
        if not ret:  
            break  

        processed_frame = preprocess_frame(frame)  
        results = model(processed_frame)  

        # در اینجا فقط اجسام متحرک را بررسی می‌کنیم  
        current_sperms = 0  
        for *box, conf, cls in results.xyxy[0]:  
            if conf > 0.1 and int(cls) == 0:  
                current_sperms += 1  

        # اگر فریم قبلی وجود داشته باشد، بررسی کنیم که آیا اسپرم‌ها حرکت کرده‌اند  
        if previous_frame is not None:  
            movement_detected = np.abs(current_sperms - previous_frame) > 0  
            if movement_detected:  
                total_moving_sperms += current_sperms  
        
        previous_frame = current_sperms  
        
        cv2.putText(frame, f"Moving Sperms: {total_moving_sperms}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  
        show_image(frame, "Frame with Detected Moving Sperms")  

    video.release()  
    return total_moving_sperms  

def main():  
    root = tk.Tk()  
    root.withdraw()  

    video_path = filedialog.askopenfilename(title="انتخاب فایل ویدیو", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])  
    if not video_path:  
        return  

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  

    total_moving_sperms = detect_moving_sperms(model, video_path)  

    messagebox.showinfo("نتیجه", f"تعداد اسپرم‌های متحرک: {total_moving_sperms}")  

if __name__ == "__main__":  
    main()
