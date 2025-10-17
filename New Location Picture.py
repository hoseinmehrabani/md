import cv2
import geocoder
from datetime import datetime


def take_photo(filename):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()


def get_location():
    g = geocoder.ip('me')
    return g.latlng


def main():
    filename = 'selfie.jpg'

    # اولین عکس را بگیرید
    print("Taking the photo...")
    take_photo(filename)
    print(f"Photo taken: {filename}")

    # لوکیشن کاربر را دریافت کنید
    current_location = get_location()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Current location: {current_location}")
    print(f"Timestamp: {timestamp}")


if __name__ == "__main__":
    main()
