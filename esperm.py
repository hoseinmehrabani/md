import cv2
import numpy as np
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename

# پنجره انتخاب فایل
Tk().withdraw()
video_path = askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])

if not video_path:
    print("هیچ ویدیویی انتخاب نشد.")
    exit()

# پارامترها برای تشخیص حرکت
params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

cap = cv2.VideoCapture(video_path)
ret, old_frame = cap.read()
if not ret:
    print("خطا در باز کردن ویدیو.")
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **params)

# ماسک و ردیابی
mask = np.zeros_like(old_frame)
tracked_sperms = {i: {'positions': [], 'speeds': [], 'total_distance': 0, 'alive': False} for i in range(len(p0))}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    if p1 is not None and p0 is not None:
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            distance = np.sqrt((a - c) ** 2 + (b - d) ** 2)

            # شرط برای اسپرم زنده
            speed = distance
            if speed > 2:  # اسپرم زنده با حداقل سرعت 2
                tracked_sperms[i]['alive'] = True
            
            # به‌روزرسانی اطلاعات اسپرم
            tracked_sperms[i]['positions'].append((a, b))
            tracked_sperms[i]['speeds'].append(speed)
            tracked_sperms[i]['total_distance'] += distance

            mask = cv2.circle(mask, (int(a), int(b)), 5, (0, 255, 0), -1)
            frame = cv2.add(frame, mask)

        # شماره‌گذاری اسپرم‌های زنده
        for idx, data in tracked_sperms.items():
            if data['alive']:
                pos = data['positions'][-1]
                cv2.putText(frame, f"{idx}", (int(pos[0]), int(pos[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow("Sperm Tracking with IDs", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cap.release()
cv2.destroyAllWindows()

# محاسبه تعداد اسپرم‌های زنده
alive_sperms_count = sum(1 for sperm in tracked_sperms.values() if sperm['alive'])

# نمایش تعداد اسپرم‌های زنده در پیام‌باکس
Tk().withdraw()  # برای جلوگیری از باز شدن پنجره اصلی tkinter
messagebox.showinfo("تعداد اسپرم‌های سالم", f"تعداد اسپرم‌های سالم و مولد: {alive_sperms_count}")

# پیدا کردن اسپرم با بیشترین جابجایی
most_moving_sperm = max(
    [sperm for sperm in tracked_sperms.values() if sperm['alive']],
    key=lambda x: x['total_distance'],
    default=None
)

if most_moving_sperm:
    final_position = most_moving_sperm['positions'][-1]
    print(f"لوکیشن اسپرمی که بیشترین جابجایی داشته و زنده است: {final_position} با مجموع جابجایی {most_moving_sperm['total_distance']}")
else:
    print("هیچ اسپرم زنده‌ای با جابجایی بالا پیدا نشد.")
