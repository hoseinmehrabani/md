import cv2  
import numpy as np  

# تابع برای شناسایی اشیاء رنگ مشکی  
def detect_black_objects(frame):  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    
    # تعریف محدوده رنگ مشکی در فضای HSV  
    lower_black = np.array([0, 0, 0])        # حد پایین رنگ مشکی  
    upper_black = np.array([180, 255, 30])   # حد بالا رنگ مشکی  

    # ایجاد ماسک برای رنگ مشکی  
    mask = cv2.inRange(hsv, lower_black, upper_black)  

    return mask  

# تابع برای بررسی الگوی حرکت  
def analyze_movement(previous_position, current_position):  
    dx = current_position[0] - previous_position[0]  
    dy = current_position[1] - previous_position[1]  
    
    if abs(dy) < 20 and dx > 0:  
        return "forward"  
    elif abs(dx) > abs(dy):  
        return "circular"  
    return "stationary"  

# تنظیم زمان پردازش  
start_time = 3000  # آغاز از 3 ثانیه  
end_time = 10000   # پایان در 10 ثانیه  

# باز کردن ویدیو  
cap = cv2.VideoCapture('video_2024-10-26_21-41-50.mp4')  
cap.set(cv2.CAP_PROP_POS_MSEC, start_time)  

object_count = 0  
forward_count = 0  
circular_count = 0  
prev_positions = {}  
frame_count = 0  
esperm = 0

# بارگذاری تصویر مرجع  
template = cv2.imread('Untitled1.png', 0)  
w, h = template.shape[::-1]  

# زمانی که ویدیو باز است  
while cap.isOpened():  
    ret, frame = cap.read()  
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)  

    if not ret or current_time > end_time:  
        break  
    
    mask = detect_black_objects(frame)  
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
    
    for cnt in contours:  
        area = cv2.contourArea(cnt)  
        if area > 500:  
            object_count += 1  
            M = cv2.moments(cnt)  
            if M["m00"] != 0:  
                cX = int(M["m10"] / M["m00"])  
                cY = int(M["m01"] / M["m00"])  
                
                object_id = f'obj_{object_count}'  
                if object_id in prev_positions:  
                    movement_type = analyze_movement(prev_positions[object_id], (cX, cY))  
                    if movement_type == "forward":  
                        forward_count += 1  
                    elif movement_type == "circular":  
                        circular_count += 1  
                
                prev_positions[object_id] = (cX, cY)  

                # تطبیق شیء با تصویر مرجع
                x, y, w, h = cv2.boundingRect(cnt)
                object_img = frame[y:y+h, x:x+w]
                object_gray = cv2.cvtColor(object_img, cv2.COLOR_BGR2GRAY)
                
                # بررسی اندازه تصویر
                if object_gray.shape[0] >= template.shape[0] and object_gray.shape[1] >= template.shape[1]:
                    res = cv2.matchTemplate(object_gray, template, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.8
                    loc = np.where(res >= threshold)
                    if len(loc[0]) > 0:
                        esperm += 1

    frame_count += 1  

cap.release()  
cv2.destroyAllWindows()  

# نتایج نهایی  
print(f"Total objects detected: {object_count}")  
print(f"Forward movement objects: {forward_count}")  
print(f"Circular movement objects: {circular_count}")  
print(f"Esperm count: {esperm}")
