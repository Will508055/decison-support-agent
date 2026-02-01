import geocoder
from geopy.geocoders import Nominatim
from weather_wise.weather_wise import WeatherWise

def get_zip_code() -> str:
    ip_loc = geocoder.ip('me')
    lat, long = ip_loc.latlng
    geolocator = Nominatim(user_agent="zip_code_locator")
    location = geolocator.reverse((lat, long), language='en')
    return location.raw['address']['postcode']

def get_weather_info(zip_code: str) -> dict:
    weather = WeatherWise(zip_code)
    weather_dict = weather._get_weather_data()
    weather_dict['temperature'] = str(weather_dict['temperature']) + ' °' + weather_dict['temperature_unit']
    keys_to_remove = ['icon', 'detailed_forecast', 'temperature_unit', 'wind_direction']
    for key in keys_to_remove:
        weather_dict.pop(key, None)
    return weather_dict