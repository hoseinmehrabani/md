import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
import matplotlib.pyplot as plt
from tensorflow.keras.applications import InceptionV3
from scipy.linalg import sqrtm

# تنظیمات
EPOCHS = 10000
BATCH_SIZE = 100
LEARNING_RATE = 0.0002
NOISE_DIM = 100
FEATURE_DIM_2D = 3  # تعداد ویژگی‌های 2 بعدی
FEATURE_DIM_3D = 3  # تعداد ویژگی‌های 3 بعدی


# مدل ساده شبکه WGAN
def create_generator():
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_dim=NOISE_DIM + FEATURE_DIM_2D + FEATURE_DIM_3D))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(28 * 28 * 1, activation='tanh'))
    model.add(layers.Reshape((28, 28, 1)))
    return model


def create_discriminator():
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=(28, 28, 1)))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(1))  # خروجی خطی برای WGAN
    return model


def wasserstein_loss(y_true, y_pred):
    return tf.reduce_mean(y_true * y_pred)


# محاسبه FID
def calculate_fid(real_images, fake_images):
    # بارگذاری مدل InceptionV3
    model = InceptionV3(include_top=False, pooling='avg', input_shape=(28, 28, 1))

    # استخراج ویژگی‌ها
    real_features = model.predict(real_images)
    fake_features = model.predict(fake_images)

    # محاسبه میانگین و کوواریانس
    mu_real, sigma_real = real_features.mean(axis=0), np.cov(real_features, rowvar=False)
    mu_fake, sigma_fake = fake_features.mean(axis=0), np.cov(fake_features, rowvar=False)

    # محاسبه FID
    fid = np.sum((mu_real - mu_fake) ** 2) + np.trace(
        sigma_real + sigma_fake - 2 * sqrtm(np.dot(sigma_real, sigma_fake)))
    return fid


# آموزش WGAN
def train_wgan(generator, discriminator, real_images, epochs=EPOCHS, batch_size=BATCH_SIZE):
    discriminator.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                          loss=wasserstein_loss)

    for epoch in range(epochs):
        for _ in range(5):  # آموزش تمییزدهنده بیشتر
            noise = np.random.normal(0, 1, size=[batch_size, NOISE_DIM])
            features = np.random.rand(batch_size, FEATURE_DIM_2D + FEATURE_DIM_3D)
            input_data = np.concatenate([noise, features], axis=1)

            generated_images = generator.predict(input_data)

            real_images_batch = real_images[np.random.randint(0, real_images.shape[0], size=batch_size)]
            combined_images = np.concatenate([generated_images, real_images_batch])

            labels = np.concatenate([np.ones(batch_size), -np.ones(batch_size)])  # برچسب‌ها برای WGAN
            discriminator.train_on_batch(combined_images, labels)

        noise = np.random.normal(0, 1, size=[batch_size, NOISE_DIM])
        features = np.random.rand(batch_size, FEATURE_DIM_2D + FEATURE_DIM_3D)
        input_data = np.concatenate([noise, features], axis=1)
        generator_loss = generator.train_on_batch(input_data, np.ones(batch_size))  # برچسب‌ها برای تولید

        if epoch % 1000 == 0:
            print(f'Epoch {epoch} completed - Generator loss: {generator_loss}')

            # محاسبه FID
            fid = calculate_fid(real_images_batch, generated_images)
            print(f'FID: {fid}')


# ورود اطلاعات از کاربر
shop_type = input("نوع فروشگاه خود را وارد کنید (مثلا: لباس، الکترونیک): ")
area = input("متراژ فروشگاه خود را وارد کنید (متر مربع): ")
color_style = input("رنگ و سبک را به صورت عددی وارد کنید (به عنوان مثال: 0.1 0.2 0.3): ")
dimensionality_2d = input("ویژگی‌های 2 بعدی (دو عدد) را وارد کنید (مثلا: 0.1 0.2): ")
dimensionality_3d = input("ویژگی‌های 3 بعدی (سه عدد) را وارد کنید (مثلا: 0.1 0.2 0.3): ")

features = np.array([
    list(map(float, color_style.split())) +
    list(map(float, dimensionality_2d.split())) +
    list(map(float, dimensionality_3d.split()))
])

# تولید طرح
generator = create_generator()
discriminator = create_discriminator()

# بارگذاری داده‌های واقعی
(x_train, _), (_, _) = tf.keras.datasets.mnist.load_data()
x_train = (x_train.astype(np.float32) - 127.5) / 127.5  # نرمال‌سازی داده‌ها
x_train = np.expand_dims(x_train, axis=-1)

train_wgan(generator, discriminator, x_train)

# تولید تصویر جدید با ویژگی‌های اضافی
noise = np.random.normal(0, 1, size=[1, NOISE_DIM])
input_data = np.concatenate([noise, features], axis=1)  # ادغام نویز و ویژگی‌های اضافی
generated_image = generator.predict(input_data)

# نمایش تصویر
plt.imshow(generated_image[0, :, :, 0], cmap='gray')
plt.axis('off')
plt.show()
