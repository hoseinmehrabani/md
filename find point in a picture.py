import cv2
import numpy as np

def detect_points(image_path, threshold_value=240, min_distance=10):
    # بارگذاری تصویر
    image = cv2.imread(image_path)
    if image is None:
        print("عدم توانایی بارگذاری تصویر. لطفاً مسیر تصویر را بررسی کنید.")
        return

    # تبدیل به مقیاس خاکستری
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # تعیین آستانه برای شناسایی نقاط
    _, thresholded = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # پیدا کردن مختصات نقاط
    coords = np.column_stack(np.where(thresholded > 0))

    if len(coords) == 0:
        print("نقطه‌ای پیدا نشد.")
        return

    # شناسایی و شمارش نقاط یکتا
    unique_points = []
    for (y, x) in coords:
        if not any(np.linalg.norm(np.array([y, x]) - np.array(up)) < min_distance for up in unique_points):
            unique_points.append((y, x))

    if len(unique_points) == 0:
        print("نقطه‌ای یکتا پیدا نشد.")
        return

    # چاپ مختصات و رنگ نقاط
    for (y, x) in unique_points:
        color = image[y, x].tolist()
        print(f"موقعیت نقطه: ({x}, {y}) | رنگ: {color}")
        cv2.circle(image, (x, y), 7, (0, 0, 255), -1)  # دایره قرمز رنگ روی نقاط یکتا

    # نمایش تصویر با نقاط شناسایی‌شده
    cv2.imshow("Detected Points", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ذخیره تصویر با علامت‌گذاری
    output_path = input("نام تصویر خروجی (با فرمت .jpg یا .png): ")
    cv2.imwrite(output_path, image)
    print(f"تصویر با نقاط شناسایی‌شده ذخیره شد: {output_path}")

# مسیر تصویر و مقدار آستانه
image_path = 'C:\\Users\\hosein\\Desktop\\Untitled.png'  # مسیر صحیح را وارد کنید
detect_points(image_path, threshold_value=200, min_distance=10)