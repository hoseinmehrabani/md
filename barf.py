# نماده‌های پایتون و فریم‌ورک‌ها
symbols = {"❤","🐍", "🌐", "📦", "🔗", "📊"}
print(symbols)
# تصویر برف
snow_image = """
❄️❄️❄️❄️❄️❄️❄️❄️❄️❄️
❄️❄️❄️❄️❄️❄️❄️❄️❄️❄️
❄️❄️❄️❄️❄️❄️❄️❄️❄️❄️
❄️❄️❄️❄️❄️❄️❄️❄️❄️❄️
❄️❄️❄️❄️❄️❄️❄️❄️❄️❄️
"""
while True:
    # ترکیب نماده‌ها با برف
    for symbol in symbols:
        snow_image = snow_image.replace("❄️", symbol)
        print(snow_image)
