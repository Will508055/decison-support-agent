from src import weather
from src import date_time
from src import get_images
from src import llm_calls
import asyncio
from src import vector_db as db
from src import save_recs


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


async def get_recommendation(weather, date_time, image_path):
    with open(image_path, 'rb') as img_file:
        image = img_file.read()

    tasks = [
        llm_calls.describe_conditions(weather, date_time),
        llm_calls.describe_scene(image)
    ]

    inputs = await asyncio.gather(*tasks)
    conditions = inputs[0]
    scene = inputs[1]

    db.update_vector_db()
    context = db.query_vector_db(conditions=conditions, scene=scene)

    recommendation = llm_calls.recommend_approach(inputs[0], inputs[1], context)

    return recommendation


def save_recommendation(conditions, scene, recommendation):
    save_recs.save_recs(conditions, scene, recommendation)
    return None