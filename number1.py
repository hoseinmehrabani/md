import cv2  
import os  

# بارگذاری تصویر  
our_image = cv2.imread("Untitled.png", 0)  

# بررسی بارگذاری موفقیت‌آمیز تصویر  
if our_image is None:  
    print("Error: Image could not be loaded. Please check the file path.")  
else:  
    # اندازه تصویر  
    height, width = our_image.shape  

    # محاسبه ابعاد هر قسمت  
    img_height = height // 3  
    img_width = width // 3  

    # ایجاد دایرکتوری برای ذخیره قسمت‌ها  
    output_dir = "output_images"  
    os.makedirs(output_dir, exist_ok=True)  

    # تقسیم کردن تصویر به نه قسمت  
    for i in range(3):  
        for j in range(3):  
            # محاسبه مختصات هر قسمت  
            y_start = i * img_height  
            y_end = (i + 1) * img_height  
            x_start = j * img_width  
            x_end = (j + 1) * img_width  

            # برش تصویر  
            img_part = our_image[y_start:y_end, x_start:x_end]  

            # شماره‌گذاری قسمت  
            part_number = i * 3 + j + 1  
            output_filename = f"{output_dir}/part_{part_number}.jpeg"  

            # ذخیره کردن قسمت  
            cv2.imwrite(output_filename, img_part)  

            print(f"Saved: {output_filename}")
