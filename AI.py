from bs4 import BeautifulSoup
from langdetect import detect
from gtts import gTTS
import os
import playsound
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rich.console import Console
from rich.table import Table

# بارگذاری NLTK
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

console = Console()


# پیش‌پردازش متن
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    return ' '.join(lemmatized_words)


# تابع برای جستجوی پاسخ در یک سایت مرجع
def search_answer_from_reference(query, reference_url):
    try:
        response = requests.get(reference_url, params={'q': query})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # تنظیم انتخابگر CSS به‌روز
            answer = soup.select_one('div.h')  # این انتخابگر را با انتخابگر مناسب جایگزین کنید
            if answer:
                return answer.text.strip()
    except Exception as e:
        print(f"Error fetching from reference site: {e}")
    return None


# تابع برای جستجوی پاسخ از دیگر سایت‌ها
def search_answer_from_other_sources(query):
    BING_API_KEY = 'YOUR_BING_API_KEY'  # کلید API خود را وارد کنید
    headers = {'Ocp-Apim-Subscription-Key': BING_API_KEY}
    url = f"https://api.bing.microsoft.com/v7.0/search?q={query}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        results = response.json().get('webPages', {}).get('value', [])
        if results:
            return results[0]['snippet']  # فقط برش اول را برمی‌گردانیم
    return None


# تابع برای تبدیل متن به صدا
def text_to_speech(text, lang='fa'):
    tts = gTTS(text=text, lang=lang)
    tts.save("answer.mp3")
    playsound.playsound("answer.mp3")
    os.remove("answer.mp3")


# تابع برای ایجاد جدول تاریخچه
def display_history(history):
    table = Table(title="History")
    table.add_column("Question", style="cyan")
    table.add_column("Answer", style="magenta")

    for q, a in history:
        table.add_row(q, a)
    console.print(table)
# تابع اصلی
def main():
    reference_url = 'https://example.com/search'  # URL سایت مرجع خود را وارد کنید
    history = []

    while True:
        question = input("سوال خود را بپرسید (یا 'خروج' برای پایان): ")
        if question.lower() == 'خروج':
            break

        # پیش‌پردازش سوال
        preprocessed_question = preprocess_text(question)

        # تشخیص زبان
        lang = detect(question)

        # جستجوی پاسخ از سایت مرجع
        answer = search_answer_from_reference(preprocessed_question, reference_url)

        if not answer:
            # اگر پاسخی از سایت مرجع پیدا نشد، جستجو از دیگر منابع
            answer = search_answer_from_other_sources(preprocessed_question)

        if answer:
            print(f"پاسخ: {answer}")
            history.append((question, answer))
            text_to_speech(answer, lang)
        else:
            print("متاسفانه پاسخی پیدا نشد.")
            text_to_speech("متاسفانه پاسخی پیدا نشد.", lang)

        # نمایش تاریخچه
        display_history(history)


if __name__ == "__main__":
    main()
