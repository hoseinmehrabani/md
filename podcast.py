import requests
import pygame
import xml.etree.ElementTree as ET


# تابعی برای دریافت پادکست‌ها از RSS feed
def get_podcasts(feed_url):
    response = requests.get(feed_url)
    print(f"HTTP Status Code: {response.status_code}")  # چاپ کد وضعیت HTTP

    if response.status_code != 200:
        print("خطا در دریافت پادکست‌ها")
        return []

    # چاپ محتوای RSS برای بررسی
    print("محتوای RSS دریافتی:")
    print(response.content.decode('utf-8'))  # چاپ محتوای پاسخ به صورت رشته

    # پردازش XML برای استخراج عنوان و URL صوتی
    root = ET.fromstring(response.content)
    podcasts = []
    for item in root.findall('.//item'):
        title = item.find('title').text
        audio_url = item.find('enclosure').get('url')
        podcasts.append({'title': title, 'audio_url': audio_url})

    return podcasts


# تابعی برای پخش پادکست
def play_podcast(audio_url):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_url)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue


# URL RSS feed پادکست
PODCAST_FEED_URL = 'https://rss.art19.com/apology-line'  # URL واقعی پادکست

# اجرای برنامه
if __name__ == "__main__":
    podcasts = get_podcasts(PODCAST_FEED_URL)

    if not podcasts:
        print("هیچ پادکستی یافت نشد.")
    else:
        print("لیست پادکست‌ها:")
        for idx, podcast in enumerate(podcasts):
            print(f"{idx + 1}. {podcast['title']}")

        choice = int(input("شماره پادکست را برای پخش انتخاب کنید: ")) - 1

        if 0 <= choice < len(podcasts):
            print(f"پخش: {podcasts[choice]['title']}")
            play_podcast(podcasts[choice]['audio_url'])
        else:
            print("انتخاب نامعتبر.")