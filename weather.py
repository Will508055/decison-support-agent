import geocoder
from geopy.geocoders import Nominatim
from weather_wise.weather_wise import WeatherWise


# Get the zip code based on the device's IP address
def get_zip_code() -> str:
    try:
        ip_loc = geocoder.ip('me')
        lat, long = ip_loc.latlng
        geolocator = Nominatim(user_agent="zip_code_locator")
        location = geolocator.reverse((lat, long), language='en')
        return location.raw['address']['postcode']
    except Exception as e:
        print(f'Error obtaining zip code from IP: {e}')
        print('Defaulting to Branson, MO.')
        return '65615'

# Get the current weather conditions for the device's location
def get_weather_info(zip_code: str) -> dict:
    try:
        weather = WeatherWise(zip_code)
        weather_dict = weather.get_current_conditions()
        weather_dict['temperature'] = str(weather_dict['temperature']) + ' °' + weather_dict['temperature_unit']
        keys_to_remove = ['icon', 'detailed_forecast', 'temperature_unit', 'wind_direction']
        for key in keys_to_remove:
            weather_dict.pop(key, None)
        return weather_dict
    except Exception as e:
        print(f'Error obtaining local weather data: {e}')
        print('Defaulting to perfect weather in Branson, MO.')
        return {'short_forecast': 'Sunny',
                'temperature': '75 °F',
                'probability_of_precipitation': 0,
                'relative_humidity': 50,
                'wind_speed': '10 mph'}