import folium
import requests
from geopy.geocoders import Nominatim


class MapApp:
    def __init__(self, api_key):
        self.geolocator = Nominatim(user_agent="map_app")
        self.api_key = api_key

    def get_location(self, address):
        location = self.geolocator.geocode(address)
        return (location.latitude, location.longitude) if location else None

    def create_map(self, center, zoom=12):
        map_ = folium.Map(location=center, zoom_start=zoom, tiles='Stamen Terrain')
        folium.Marker(location=center, popup="مرکز").add_to(map_)
        return map_

    def add_marker(self, map_, location, name, details):
        folium.Marker(location=location, popup=f"{name}<br>{details}", icon=folium.Icon(color='blue')).add_to(map_)

    def save_map(self, map_, filename):
        map_.save(filename)

    def get_directions(self, origin, destination):
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            directions = response.json()
            if directions['status'] == 'OK':
                return directions['routes'][0]['legs'][0]['steps']
            else:
                print("خطا در دریافت اطلاعات مسیریابی:", directions['status'])
        else:
            print("خطا در درخواست:", response.status_code)

    def plot_directions_on_map(self, map_, steps):
        for step in steps:
            start_location = step['start_location']
            end_location = step['end_location']
            folium.Marker(location=[start_location['lat'], start_location['lng']], popup=step['html_instructions'],
                          icon=folium.Icon(color='green')).add_to(map_)
            folium.PolyLine(
                [(start_location['lat'], start_location['lng']), (end_location['lat'], end_location['lng'])],
                color='blue', weight=2.5, opacity=1).add_to(map_)

    def search_nearby_places(self, location):
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location[0]},{location[1]}&radius=1500&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            places = response.json()
            return places['results'] if places['status'] == 'OK' else []
        else:
            print("خطا در درخواست:", response.status_code)
            return []


if __name__ == "__main__":
    API_KEY = "YOUR_API_KEY"  # API Key خود را وارد کنید
    app = MapApp(API_KEY)

    # وارد کردن آدرس مبدا و مقصد
    origin_address = input("آدرس مبدا را وارد کنید: ")
    destination_address = input("آدرس مقصد را وارد کنید: ")

    origin = app.get_location(origin_address)
    destination = app.get_location(destination_address)

    if origin and destination:
        map_ = app.create_map(origin)

        # جستجوی مکان‌های نزدیک
        nearby_places = app.search_nearby_places(origin)
        for place in nearby_places:
            name = place['name']
            location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
            app.add_marker(map_, location, name, place.get('vicinity', 'جزئیات موجود نیست'))

        # دریافت و نمایش مسیر
        directions = app.get_directions(f"{origin[0]},{origin[1]}", f"{destination[0]},{destination[1]}")
        if directions:
            app.plot_directions_on_map(map_, directions)

        app.add_marker(map_, origin, "مبدا", "")
        app.add_marker(map_, destination, "مقصد", "")

        app.save_map(map_, "map_with_directions_and_places.html")
        print("نقشه با موفقیت ذخیره شد! فایل map_with_directions_and_places.html را باز کنید.")
    else:
        print("آدرس نامعتبر است.")
