import numpy as np
import cv2
from PIL import Image
import random


# بارگذاری تصاویر کوچک
def load_images(image_paths):
    images = []
    for path in image_paths:
        img = Image.open(path).resize((random.randint(20, 40), random.randint(20, 40)))
        images.append(np.array(img))
    return images


# اضافه کردن فیلتر به تصویر
def apply_filter(image):
    return cv2.GaussianBlur(image, (5, 5), 0)  # بلور


# تغییر رنگ
def change_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[..., 0] = (hsv[..., 0] + random.randint(-10, 10)) % 180  # تغییر رنگ
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


# جایگزینی پیکسل‌ها با اشیاء
def replace_with_images(image, small_images, texts):
    height, width, _ = image.shape
    output_image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(0, height, 32):
        for x in range(0, width, 32):
            selected_image = random.choice(small_images)
            output_image[y:y + 32, x:x + 32] = selected_image

            # اعمال فیلتر
            if random.random() < 0.5:  # 50% احتمال اعمال فیلتر
                output_image[y:y + 32, x:x + 32] = apply_filter(selected_image)

            # اضافه کردن متن
            if random.random() < 0.3:  # 30% احتمال اضافه کردن متن
                selected_text = random.choice(texts)
                font_size = random.uniform(0.4, 1.0)  # اندازه تصادفی
                color = tuple(random.randint(0, 255) for _ in range(3))  # رنگ تصادفی
                cv2.putText(output_image, selected_text, (x, y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1)

    return change_color(output_image)


# بارگذاری تصاویر و متن‌ها
input_image = cv2.imread('input_image.jpg')
miniature_image_paths = ['miniature1.png', 'miniature2.png', 'miniature3.png']
icon_image_paths = ['icon1.png', 'icon2.png', 'icon3.png']
digital_painting_paths = ['painting1.png', 'painting2.png', 'painting3.png']
collage_paths = ['collage1.png', 'collage2.png', 'collage3.png']

# بارگذاری تمام تصاویر
miniature_images = load_images(miniature_image_paths)
icon_images = load_images(icon_image_paths)
digital_paintings = load_images(digital_painting_paths)
collage_images = load_images(collage_paths)

# ترکیب تمام تصاویر
all_images = miniature_images + icon_images + digital_paintings + collage_images

# متن‌های کوچک
texts = ["زندگی زیباست", "خلاقیت بی‌پایان", "هر روز یک فرصت جدید"]

# جایگزینی پیکسل‌ها با تصاویر کوچک و متن
output_image = replace_with_images(input_image, all_images, texts)

# نمایش تصویر نهایی
Image.fromarray(output_image).show()
