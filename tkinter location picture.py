import cv2
import geocoder
import time
import threading
from tkinter import *
from PIL import Image, ImageTk


class SelfieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selfie App")

        self.photo_label = Label(root)
        self.photo_label.pack()

        self.location_label = Label(root, text="Location: ", font=("Helvetica", 14))
        self.location_label.pack()

        self.take_photo_button = Button(root, text="Take Photo", command=self.take_photo)
        self.take_photo_button.pack()

        self.previous_location = None
        self.running = True

        # شروع یک ترد برای بررسی مکان
        threading.Thread(target=self.track_location, daemon=True).start()

    def take_photo(self):
        filename = 'selfie.jpg'
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            self.show_photo(filename)
        cap.release()

    def show_photo(self, filename):
        img = Image.open(filename)
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.photo_label.config(image=img)
        self.photo_label.image = img

    def get_location(self):
        g = geocoder.ip('me')
        return g.latlng  # عرض و طول جغرافیایی

    def track_location(self):
        while self.running:
            current_location = self.get_location()
            if current_location != self.previous_location:
                self.previous_location = current_location
                self.location_label.config(text=f"Location: {current_location}")
            time.sleep(10)  # فاصله بین بررسی مکان‌ها

    def on_closing(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = SelfieApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
