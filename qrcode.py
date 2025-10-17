import qrcode
from PIL import Image, ImageDraw, ImageFont

def create_custom_qr_code(data, logo_path=None, output_path='custom_qr_code.png'):
    # تنظیمات QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # ایجاد تصویر QR Code
    qr_image = qr.make_image(fill_color="#1E90FF", back_color="white")

    # اگر لوگویی داده شده باشد، آن را روی QR Code قرار دهیم
    if logo_path:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")

        # تنظیم اندازه لوگو
        logo_size = 60
        logo = logo.resize((logo_size, logo_size))

        # قرار دادن لوگو در وسط QR Code
        qr_width, qr_height = qr_image.size
        logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        # ترکیب QR Code و لوگو
        qr_image.paste(logo, logo_position, logo)

    # افزودن متن سفارشی به تصویر
    draw = ImageDraw.Draw(qr_image)
    font = ImageFont.load_default()  # می‌توانید فونت دلخواه را بارگذاری کنید
    text = "Scan Me!"  # متن سفارشی
    text_size = draw.textsize(text, font=font)
    text_position = ((qr_width - text_size[0]) // 2, qr_height - text_size[1] - 10)
    draw.text(text_position, text, fill="#FF4500", font=font)

    # ذخیره تصویر نهایی
    qr_image.save(output_path)
    print(f"Custom QR code saved as {output_path}")

# مثال استفاده
if __name__ == "__main__":
    data = "https://example.com"
    logo_path = "logo.png"  # مسیر به لوگو (می‌توانید لوگوی دلخواه خود را قرار دهید)
    create_custom_qr_code(data, logo_path, 'custom_qr_code_with_logo.png')
