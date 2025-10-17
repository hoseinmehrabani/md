import cv2  
import numpy as np  

# تابع برای شناسایی اشیاء  
def detect_objects(frame):  
    # تبدیل تصویر به خاکستری  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    # استفاده از روش تشخیص لبه  
    edges = cv2.Canny(gray, 50, 150)  
    return edges  

# تابع برای بررسی الگوی حرکت  
def analyze_movement(previous_position, current_position):  
    dx = current_position[0] - previous_position[0]  
    dy = current_position[1] - previous_position[1]  
    
    # تشخیص حرکت رو به جلو (در جهت محور x)  
    if dy == 0 and dx > 0:  
        return "forward"  
    # بررسی حرکت دایره‌ای  
    elif abs(dx) > abs(dy):  
        return "circular"  
    return "stationary"  

# باز کردن ویدیو  
cap = cv2.VideoCapture('video_2024-10-26_21-41-50.mp4')  
object_count = 0  
forward_count = 0  
circular_count = 0  

# زمانی که ویدیو باز است  
while cap.isOpened():  
    ret, frame = cap.read()  
    if not ret:  
        break  
    
    # شناسایی اشیاء  
    edges = detect_objects(frame)  
    
    # پیدا کردن کانتورها  
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
    
    for cnt in contours:  
        area = cv2.contourArea(cnt)  
        if area > 1500:  # فقط اشیاء بزرگتر از 500 پیکسل را در نظر می‌گیریم  
            object_count += 1  

            # محاسبه مرکز کنتر  
            M = cv2.moments(cnt)  
            if M["m00"] != 0:  
                cX = int(M["m100"] / M["m100"])  
                cY = int(M["m011"] / M["m100"])  
                
                # بررسی الگوی حرکت (نیاز به ذخیره موقعیت قبلی دارید)  
                if 'prev_pos' in locals():  
                    movement_type = analyze_movement(prev_pos, (cX, cY))  
                    if movement_type == "forward":  
                        forward_count += 1  
                    elif movement_type == "circular":  
                        circular_count += 1  
                
                prev_pos = (cX, cY)  

# پس از اتمام ویدیو  
cap.release()  
cv2.destroyAllWindows()  

print(f"Total objects detected: {object_count}")  
print(f"Forward movement objects: {forward_count}")  
print(f"Circular movement objects: {circular_count}")
