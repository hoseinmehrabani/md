import cv2
import geocoder
import time

def take_photo(filename):
    # استفاده از وب‌کم برای گرفتن عکس
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()

def get_location():
    # گرفتن لوکیشن با geocoder
    g = geocoder.ip('me')
    return g.latlng  # برگرداندن عرض و طول جغرافیایی

def main():
    previous_location = None

    while True:
        # عکس گرفتن
        filename = 'selfie.jpg'
        take_photo(filename)
        print(f"Photo taken: {filename}")

        # گرفتن لوکیشن
        current_location = get_location()
        print(f"Current location: {current_location}")

        # بررسی تغییر مکان
        if current_location != previous_location:
            print("Location changed!")
            previous_location = current_location

        # فاصله بین عکس‌ها (مثلاً 10 ثانیه)
        time.sleep(10)

if __name__ == "__main__":
    main()
