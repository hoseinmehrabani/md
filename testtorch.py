"""import cv2  
import torch  

print(cv2.__version__)  # این باید نسخه OpenCV را چاپ کند  
print(torch.__version__)  # این باید نسخه PyTorch را چاپ کند
"""
import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# پنجره انتخاب فایل
Tk().withdraw()  # مخفی کردن پنجره اصلی tkinter
video_path = askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])

if not video_path:
    print("هیچ ویدیویی انتخاب نشد.")
    exit()

# پارامترها برای تشخیص حرکت اسپرم‌های مولد
params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# بارگذاری ویدیو انتخاب شده
cap = cv2.VideoCapture(video_path)
ret, old_frame = cap.read()
if not ret:
    print("خطا در باز کردن ویدیو.")
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **params)

# ساخت ماسک برای ردیابی اسپرم‌های مولد
mask = np.zeros_like(old_frame)
tracked_sperms = {i: {'positions': [], 'speeds': []} for i in range(len(p0))} 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    if p1 is not None and p0 is not None:
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # ردیابی و محاسبه حرکت اسپرم‌ها
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            distance = np.sqrt((a - c) ** 2 + (b - d) ** 2)
            speed = distance  

            if i in tracked_sperms:
                tracked_sperms[i]['positions'].append((a, b))
                tracked_sperms[i]['speeds'].append(speed)

            mask = cv2.circle(mask, (int(a), int(b)), 5, (0, 255, 0), -1)
            frame = cv2.add(frame, mask)

    cv2.imshow("Tracked Sperm", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

# محاسبه اسپرم با بیشترین جابه‌جایی و سریع‌ترین اسپرم
most_moving_sperm = max(tracked_sperms.items(), key=lambda x: sum(x[1]['speeds']))
max_speed_sperm = max(tracked_sperms.items(), key=lambda x: max(x[1]['speeds']))

moving_sperm_id, moving_sperm_data = most_moving_sperm
max_distance = sum(moving_sperm_data['speeds'])
last_position_moving = moving_sperm_data['positions'][-1]

speed_sperm_id, speed_sperm_data = max_speed_sperm
max_speed = max(speed_sperm_data['speeds'])
max_speed_position = speed_sperm_data['positions'][speed_sperm_data['speeds'].index(max_speed)]

print(f"اسپرم با بیشترین جابه‌جایی: ID={moving_sperm_id} با جابه‌جایی کل {max_distance} در موقعیت {last_position_moving}")
print(f"سریع‌ترین اسپرم: ID={speed_sperm_id} با سرعت {max_speed} در موقعیت {max_speed_position}")

cap.release()
cv2.destroyAllWindows()
