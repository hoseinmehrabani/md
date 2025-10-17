import os
import numpy as np
import sqlite3
from PIL import Image
import tensorflow as tf
from tensorflow.keras import layers, models
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd

class FeedbackDatabase:
    """مدیریت پایگاه داده نظرات کاربران"""

    def __init__(self, db_name='feedback.db'):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """ایجاد پایگاه داده و جدول نظرات"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wall_color TEXT,
                    furniture_type TEXT,
                    user_comment TEXT,
                    design_type INTEGER,
                    sentiment_score REAL
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"خطا در ایجاد پایگاه داده: {e}")
        finally:
            conn.close()

    def save_feedback(self, wall_color, furniture_type, user_comment, design_type, sentiment_score):
        """ذخیره نظرات کاربر در پایگاه داده"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''
                INSERT INTO feedback (wall_color, furniture_type, user_comment, design_type, sentiment_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (wall_color, furniture_type, user_comment, design_type, sentiment_score))
            conn.commit()
        except Exception as e:
            print(f"خطا در ذخیره نظرات: {e}")
        finally:
            conn.close()

    def update_feedback(self, feedback_id, wall_color, furniture_type, user_comment, design_type, sentiment_score):
        """بروزرسانی نظر کاربر بر اساس ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''
                UPDATE feedback
                SET wall_color = ?, furniture_type = ?, user_comment = ?, design_type = ?, sentiment_score = ?
                WHERE id = ?
            ''', (wall_color, furniture_type, user_comment, design_type, sentiment_score, feedback_id))
            conn.commit()
        except Exception as e:
            print(f"خطا در بروزرسانی نظر: {e}")
        finally:
            conn.close()

    def delete_feedback(self, feedback_id):
        """حذف نظر کاربر بر اساس ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
            conn.commit()
        except Exception as e:
            print(f"خطا در حذف نظر: {e}")
        finally:
            conn.close()


class DesignModel:
    """مدل طراحی داخلی با استفاده از U-Net"""

    def __init__(self, input_shape=(150, 150, 3)):
        self.model = self.create_unet_model(input_shape)

    def create_unet_model(self, input_shape):
        """ایجاد مدل U-Net"""
        inputs = tf.keras.Input(shape=input_shape)
        c1 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        c1 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(c1)
        p1 = layers.MaxPooling2D((2, 2))(c1)

        c2 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(p1)
        c2 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(c2)
        p2 = layers.MaxPooling2D((2, 2))(c2)

        c3 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(p2)
        c3 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(c3)

        u4 = layers.concatenate([layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c3), c2])
        c4 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(u4)
        c4 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(c4)

        u5 = layers.concatenate([layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c4), c1])
        c5 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(u5)
        c5 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(c5)

        outputs = layers.Conv2D(1, (1, 1), activation='sigmoid')(c5)
        model = models.Model(inputs=[inputs], outputs=[outputs])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, epochs=10):
        """آموزش مدل با داده‌های بارگذاری شده"""
        try:
            train_data, val_data = self.load_data()
            history = self.model.fit(train_data, epochs=epochs, validation_data=val_data)
            return history
        except Exception as e:
            print(f"خطا در آموزش مدل: {e}")

    def load_data(self):
        """بارگذاری داده‌ها و پیش‌پردازش تصاویر"""
        try:
            datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255,
                validation_split=0.2,
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True
            )

            train_data = datagen.flow_from_directory('data_directory', target_size=(150, 150), class_mode='sparse', subset='training')
            val_data = datagen.flow_from_directory('data_directory', target_size=(150, 150), class_mode='sparse', subset='validation')
            return train_data, val_data
        except Exception as e:
            print(f"خطا در بارگذاری داده: {e}")

    def predict(self, image_path):
        """پیش‌بینی طراحی بر اساس تصویر ورودی"""
        try:
            img = Image.open(image_path).resize((150, 150))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            predictions = self.model.predict(img_array)
            return np.argmax(predictions)
        except Exception as e:
            print(f"خطا در پیش‌بینی طراحی: {e}")


class SentimentAnalyzer:
    """تحلیل احساسات نظرات کاربران"""

    @staticmethod
    def analyze(text):
        """تحلیل احساسات متن ورودی"""
        analysis = TextBlob(text)
        return analysis.sentiment.polarity  # بازگشت نمره احساسات


class FeedbackAnalyzer:
    """تجزیه و تحلیل نظرات کاربران"""

    def __init__(self, db_name='feedback.db'):
        self.db_name = db_name

    def analyze_feedback(self):
        """تجزیه و تحلیل داده‌ها و چاپ نتایج"""
        try:
            conn = sqlite3.connect(self.db_name)
            df = pd.read_sql_query("SELECT * FROM feedback", conn)
            conn.close()

            analysis = df.groupby('design_type')['sentiment_score'].mean()
            print("میانگین نمره احساسات بر اساس نوع طراحی:")
            print(analysis)

            df['comment_length'] = df['user_comment'].apply(len)
            comment_analysis = df.groupby('design_type')['comment_length'].mean()
            print("\nمیانگین طول نظرات بر اساس نوع طراحی:")
            print(comment_analysis)

            self.visualize_analysis(df)
        except Exception as e:
            print(f"خطا در تحلیل نظرات: {e}")

    def visualize_analysis(self, df):
        """نمودار توزیع نمرات احساسات و طول نظرات"""
        plt.figure(figsize=(14, 6))

        plt.subplot(1, 2, 1)
        df['sentiment_score'].hist(bins=20, color='blue', alpha=0.7)
        plt.title('توزیع نمرات احساسات')
        plt.xlabel('نمره احساسات')
        plt.ylabel('تعداد')

        plt.subplot(1, 2, 2)
        df['comment_length'].hist(bins=20, color='green', alpha=0.7)
        plt.title('توزیع طول نظرات')
        plt.xlabel('طول نظر')
        plt.ylabel('تعداد')

        plt.tight_layout()
        plt.show()

def get_user_input(prompt, valid_options):
    """مدیریت ورودی کاربر"""
    user_input = input(prompt)
    while user_input not in valid_options:
        user_input = input(f"ورود نامعتبر! {prompt}")
    return user_input

def validate_image_path(image_path):
    """بررسی اعتبار مسیر تصویر"""
    return os.path.exists(image_path)

# کد اصلی
if __name__ == "__main__":
    db = FeedbackDatabase()  # ایجاد پایگاه داده و جدول
    model = DesignModel()  # ایجاد مدل طراحی

    input_shape = (150, 150, 3)

    if os.path.exists('interior_design_model.h5'):
        model.model = tf.keras.models.load_model('interior_design_model.h5')
    else:
        model.train(epochs=10)  # تعداد ایپوک‌ها قابل تنظیم است
        model.model.save('interior_design_model.h5')

    # دریافت ورودی کاربر
    valid_wall_colors = ["قرمز", "آبی", "سبز", "زرد"]
    valid_furniture_types = ["مدرن", "کلاسیک", "قدیمی"]

    wall_color = get_user_input("رنگ دیوار را انتخاب کنید (قرمز، آبی، سبز، زرد): ", valid_wall_colors)
    furniture_type = get_user_input("نوع مبلمان را انتخاب کنید (مدرن، کلاسیک، قدیمی): ", valid_furniture_types)
    user_comment = input("نظرات شما: ")

    # تحلیل احساسات
    sentiment_score = SentimentAnalyzer.analyze(user_comment)

    image_path = 'your_image_path.jpg'  # مسیر تصویر خود را وارد کنید
    if validate_image_path(image_path):
        # پیش‌بینی طراحی
        design_type = model.predict(image_path)
        print(f"نوع طراحی پیش‌بینی‌شده: {design_type}")
    else:
        print("مسیر تصویر نامعتبر است.")

    print(f"نمره احساسات: {sentiment_score}")

    # ذخیره نظرات و پیش‌بینی‌ها در پایگاه داده
    db.save_feedback(wall_color, furniture_type, user_comment, design_type, sentiment_score)

    # تجزیه و تحلیل داده‌ها
    feedback_analyzer = FeedbackAnalyzer()
    feedback_analyzer.analyze_feedback()
