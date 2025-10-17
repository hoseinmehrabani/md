import requests

API_KEY = 'YOUR_API_KEY'  # کلید API خود را اینجا قرار دهید


def get_place_details(address):
    # URL جستجوی Places API
    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={address}&inputtype=textquery&fields=name,formatted_address,place_id,formatted_phone_number&key={API_KEY}"

    response = requests.get(search_url)
    result = response.json()

    if result['candidates']:
        place = result['candidates'][0]
        name = place.get('name', 'نامی وجود ندارد')
        formatted_address = place.get('formatted_address', 'آدرسی وجود ندارد')
        place_id = place.get('place_id', 'آیدی وجود ندارد')

        # درخواست شماره تلفن با استفاده از place_id
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}"
        details_response = requests.get(details_url)
        details_result = details_response.json()

        phone_number = details_result.get('result', {}).get('formatted_phone_number', 'شماره تلفنی وجود ندارد')

        print(f"نام: {name}")
        print(f"آدرس: {formatted_address}")
        print(f"شماره تلفن: {phone_number}")
    else:
        print("مکانی یافت نشد.")


if __name__ == "__main__":
    address = input("لطفاً آدرس مورد نظر خود را وارد کنید: ")
    get_place_details(address)
