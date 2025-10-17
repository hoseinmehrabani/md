import cv2  
import os  

# بارگذاری تصویر مرجع  
reference_image = cv2.imread("Untitled1.png", 0)  
if reference_image is None:  
    print("Error: Reference image could not be loaded. Please check the file path.")  

# بارگذاری تصویر اولیه  
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

    # شماره‌های قسمت‌هایی که باید مقیاس شوند  
    parts_to_scale = [1, 3, 7, 9]  
    scaled_images = []  

    # تقسیم کردن تصویر به نه قسمت و مقیاس کردن  
    for i in range(3):  
        for j in range(3):  
            part_number = i * 3 + j + 1  
            
            # محاسبه مختصات هر قسمت  
            y_start = i * img_height  
            y_end = (i + 1) * img_height  
            x_start = j * img_width  
            x_end = (j + 1) * img_width  

            # برش تصویر  
            img_part = our_image[y_start:y_end, x_start:x_end]  

            # اگر شماره قسمت در لیست قسمت‌های مورد نظر بود، مقیاس کنیم  
            if part_number in parts_to_scale:  
                # تغییر اندازه تصویر به ابعاد تصویر مرجع  
                scaled_part = cv2.resize(img_part, (reference_image.shape[1], reference_image.shape[0]))  
                scaled_images.append((part_number, scaled_part))  

                # ذخیره تصویر مقیاس شده  
                output_filename = f"scaled_part_{part_number}.jpeg"  
                cv2.imwrite(output_filename, scaled_part)  
                print(f"Saved scaled part: {output_filename}")  

                # بررسی شباهت با تصویر مرجع  
                similarity_score = cv2.norm(scaled_part, reference_image, cv2.NORM_L2)  
                print(f"Similarity score between part {part_number} and reference image: {similarity_score}")  

# توجه: هرچه مقدار similarity_score کمتر باشد، تصاویر بیشتر مشابه هستند.
