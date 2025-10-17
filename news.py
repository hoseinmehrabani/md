import requests

class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def get_news(self, category=None, country='us'):
        params = {
            'apiKey': self.api_key,
            'country': country,
            'category': category
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()['articles']
        else:
            print("خطا در دریافت اخبار")
            return []

def display_news(articles):
    if not articles:
        print("هیچ خبری یافت نشد.")
        return

    for i, article in enumerate(articles):
        title = article['title']
        description = article['description'] or "توضیحی موجود نیست."
        url = article['url']
        print(f"{i + 1}. {title}\n   {description}\n   [لینک: {url}]\n")

def main():
    api_key = 'YOUR_API_KEY'  # کلید API خود را اینجا قرار دهید
    news_api = NewsAPI(api_key)

    categories = {
        'top': 'مهم‌ترین اخبار',
        'strange': 'عجیب‌ترین اخبار',
        'funny': 'جالب‌ترین اخبار',
        'technology': 'تکنولوژی',
        'sports': 'ورزشی',
        'health': 'بهداشت',
        'business': 'اقتصادی',
        'entertainment': 'سرگرمی',
        'general': 'عمومی'
    }

    while True:
        print("\n--- انتخاب دسته‌بندی اخبار ---")
        for key, value in categories.items():
            print(f"{key}: {value}")
        print("0. خروج")

        category_choice = input("دسته‌بندی مورد نظر خود را وارد کنید: ")

        if category_choice == '0':
            print("خروج از برنامه.")
            break

        if category_choice == 'top':
            articles = news_api.get_news()
            display_news(articles)
        elif category_choice == 'strange':
            articles = news_api.get_news(category='entertainment')  # می‌توانید از دسته خاصی استفاده کنید
            display_news(articles)  # فرض بر این است که اخبار عجیب در این دسته وجود دارد
        elif category_choice == 'funny':
            articles = news_api.get_news(category='entertainment')
            display_news(articles)  # اخبار جالب نیز می‌تواند از این دسته بیاید
        elif category_choice in categories:
            articles = news_api.get_news(category=category_choice)
            display_news(articles)
        else:
            print("لطفاً یک گزینه صحیح وارد کنید.")

if __name__ == "__main__":
    main()
