from src import weather
from src import date_time
from src import get_images


def get_context():
    zip_code = weather.get_zip_code()
    current_weather = weather.get_weather_info(zip_code)
    current_date_time = date_time.get_date_time()
    image_paths = get_images.get_image_paths()

    return {
        'zip_code': zip_code,
        'current_weather': current_weather,
        'current_date_time': current_date_time,
        'images': image_paths
    }