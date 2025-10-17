import streamlit as st
import pandas as pd
from pymongo import MongoClient
from PIL import Image
import datetime

# اتصال به MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['car_customization_db']
collection = db['car_designs']

# عنوان
st.title("شخصی‌سازی ماشین - الهام گرفته از Forza Horizon 5")

# انتخاب نوع ماشین
car_type = st.selectbox("نوع ماشین:", ["ایرانی", "خارجی"])

# ورودی کاربر برای ویژگی‌ها
body = st.selectbox("نوع بدنه:", ["کوپه", "سدان", "SUV", "هچ بک"])
body_kit = st.selectbox("کیت بدنه:", ["استاندارد", "اسپرت", "آئرودینامیک"])
body_color = st.color_picker("رنگ بدنه:", "#FFFFFF")

# چرخ‌ها
wheels = st.selectbox("نوع چرخ:", ["عادی", "اسپرت", "بزرگ"])
wheel_color = st.color_picker("رنگ چرخ:", "#000000")

# سیستم تعلیق
suspension = st.selectbox("نوع سیستم تعلیق:", ["عادی", "اسپرت"])
suspension_height = st.slider("ارتفاع تعلیق:", 0, 10)

# موتور و گیربکس
engine_type = st.selectbox("نوع موتور:", ["NA", "توربوشارژ", "سوپرشارژ"])
engine_power = st.slider("قدرت موتور (HP):", 50, 1200)
transmission = st.selectbox("نوع گیربکس:", ["دستی", "اتوماتیک"])

# داخل ماشین
interior_seat = st.selectbox("نوع صندلی:", ["ورزشی", "چرم", "پارچه"])
interior_color = st.color_picker("رنگ داخلی:", "#FFFFFF")
audio_system = st.selectbox("سیستم صوتی:", ["استاندارد", "حرفه‌ای"])

# چراغ‌ها
lights_type = st.selectbox("نوع چراغ‌ها:", ["LED", "هالوژنی"])
lights_color = st.color_picker("رنگ چراغ‌ها:", "#FFFFFF")

# اسپویلر
spoiler = st.selectbox("نوع اسپویلر:", ["هیچ", "اسپرت", "عادی"])

# تنظیمات دینامیک
tuning_type = st.selectbox("نوع تنظیمات دینامیک:", ["جاده‌ای", "آفرود"])
tuning_details = st.text_area("جزئیات تنظیمات دینامیک:")

# بارگذاری تصویر
uploaded_file = st.file_uploader("بارگذاری تصویر ماشین:", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="تصویر بارگذاری شده", use_column_width=True)

# دکمه طراحی
if st.button("طراحی ماشین"):
    # ذخیره ویژگی‌ها و تصویر در MongoDB
    img_path = f"uploads/{uploaded_file.name}"  # مسیر ذخیره تصویر
    img.save(img_path)  # ذخیره تصویر

    collection.insert_one({
        "car_type": car_type,
        "body": body,
        "body_kit": body_kit,
        "body_color": body_color,
        "wheels": wheels,
        "wheel_color": wheel_color,
        "suspension": suspension,
        "suspension_height": suspension_height,
        "engine_type": engine_type,
        "engine_power": engine_power,
        "transmission": transmission,
        "interior_seat": interior_seat,
        "interior_color": interior_color,
        "audio_system": audio_system,
        "lights_type": lights_type,
        "lights_color": lights_color,
        "spoiler": spoiler,
        "tuning_type": tuning_type,
        "tuning_details": tuning_details,
        "image_path": img_path,
        "date": datetime.datetime.now(),
        "ratings": []  # لیست امتیازها
    })

    st.success("طراحی ماشین با موفقیت ذخیره شد!")

# نمایش طراحی‌های قبلی
if st.checkbox("نمایش طراحی‌های قبلی"):
    designs = pd.DataFrame(list(collection.find()))
    st.write(designs)

    # نمایش تصویر طراحی‌ها
    for index, row in designs.iterrows():
        st.image(row['image_path'], caption=f"طراحی {index + 1}: {row['car_type']}", use_column_width=True)

        # امتیازدهی به طراحی
        rating = st.slider(f"امتیاز به طراحی {index + 1}:", 1, 5)
        if st.button(f"ثبت امتیاز برای طراحی {index + 1}"):
            collection.update_one(
                {"_id": row["_id"]},
                {"$push": {"ratings": rating}}
            )
            st.success("امتیاز ثبت شد!")

# نظرسنجی برای نظرات و پیشنهادات
if st.checkbox("نظرسنجی"):
    feedback = st.text_area("نظر یا پیشنهاد خود را بنویسید:")
    if st.button("ارسال نظر"):
        if feedback:
            st.success("نظر شما با موفقیت ارسال شد!")
            # ذخیره نظر در یک مجموعه جدید
            feedback_collection = db['feedback']
            feedback_collection.insert_one({
                "feedback": feedback,
                "date": datetime.datetime.now()
            })
        else:
            st.error("لطفاً نظر خود را وارد کنید.")

# بستن اتصال به MongoDB
client.close()
