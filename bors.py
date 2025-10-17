import requests

class StockMarket:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_price(self, symbol):
        url = f"{self.base_url}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            time_series = data.get('Time Series (1min)', {})
            if time_series:
                latest_time = sorted(time_series.keys())[0]
                latest_price = time_series[latest_time]['1. open']
                return float(latest_price)
        print("خطا در دریافت قیمت سهام")
        return None

    def buy_stock(self, symbol, amount, price):
        total_cost = amount * price
        # اینجا می‌توانید منطق خرید را پیاده‌سازی کنید
        print(f"خرید {amount} از سهام {symbol} به قیمت {price} USD، مجموع: {total_cost} USD")

    def sell_stock(self, symbol, amount, price):
        total_sale = amount * price
        # اینجا می‌توانید منطق فروش را پیاده‌سازی کنید
        print(f"فروش {amount} از سهام {symbol} به قیمت {price} USD، مجموع: {total_sale} USD")
def main():
    api_key = 'YOUR_API_KEY'  # کلید API خود را وارد کنید
    stock_market = StockMarket(api_key)

    while True:
        print("\n--- بورس ---")
        print("1. مشاهده قیمت سهام")
        print("2. خرید سهام")
        print("3. فروش سهام")
        print("4. خروج")

        choice = input("انتخاب کنید: ")

        if choice == '1':
            symbol = input("نماد سهام را وارد کنید: ").upper()
            price = stock_market.get_stock_price(symbol)
            if price:
                print(f"قیمت سهام {symbol}: {price} USD")

        elif choice == '2':
            symbol = input("نماد سهام را وارد کنید: ").upper()
            amount = int(input("تعداد سهام را وارد کنید: "))
            price = stock_market.get_stock_price(symbol)
            if price:
                stock_market.buy_stock(symbol, amount, price)

        elif choice == '3':
            symbol = input("نماد سهام را وارد کنید: ").upper()
            amount = int(input("تعداد سهام را وارد کنید: "))
            price = stock_market.get_stock_price(symbol)
            if price:
                stock_market.sell_stock(symbol, amount, price)

        elif choice == '4':
            print("خروج از برنامه.")
            break

        else:
            print("لطفاً گزینه صحیحی را انتخاب کنید.")
