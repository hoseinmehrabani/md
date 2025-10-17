import requests

class Weather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        parameters = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=parameters)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return weather_info
        else:
            print("Error: Unable to fetch weather data.")
            return None


def display_weather(weather_info):
    if weather_info:
        print(f"City: {weather_info['city']}")
        print(f"Temperature: {weather_info['temperature']} °C")
        print(f"Description: {weather_info['description']}")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Wind Speed: {weather_info['wind_speed']} m/s")
    else:
        print("No weather information available.")


def main():
    api_key = input("Enter your OpenWeatherMap API key: ")
    weather_service = Weather(api_key)

    while True:
        print("\nWeather Application")
        city = input("Enter the city name (or type 'exit' to quit): ")
        if city.lower() == 'exit':
            break
        weather_info = weather_service.get_weather(city)
        display_weather(weather_info)


if __name__ == "__main__":
    main()
