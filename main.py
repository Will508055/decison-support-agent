from src import weather
from src import date_time
from src import read_images
from src import llm_calls
from src import vector_db as db
from src import save_recs
import asyncio


async def main():
    # Get current weather information
    zip_code = weather.get_zip_code()
    current_weather = weather.get_weather_info(zip_code)
    current_date_time = date_time.get_date_time()

    # Display weather information and prompt user to select an image
    print(f'The current weather for zip code {zip_code} at {current_date_time} is:\n{current_weather}')
    print('\nPlease select an image that depicts a plausible situation given the current weather conditions.')
    image = read_images.read_image_choice()

    # Use LLM to describe conditions and scene based on the selected image
    print('\nAnalyzing the selected image and assessing the situation...')
    tasks = [
        llm_calls.describe_conditions(),
        llm_calls.describe_scene(image)
    ]

    inputs = await asyncio.gather(*tasks)
    conditions = inputs[0]
    scene = inputs[1]

    # Update vector database if needed and query for relevant information based on the conditions and scene
    print('\nRetrieving relevant information based on the situation...')
    db.update_vector_db()
    context = db.query_vector_db(conditions=conditions, scene=scene)

    # Use LLM to recommend an approach based on the conditions, scene, and retrieved context
    print('\nGenerating final recommendation...')
    rec = llm_calls.recommend_approach(inputs[0], inputs[1], context)

    ### Print recommendation, one attribute per line
    print('\nFINAL RECOMMENDATION:\n')
    try:
        rec_data = rec.model_dump()
        for key, value in rec_data.items():
            print(f'{key}: {value}')
    except AttributeError:
        print(rec)

    ### Ask user if they want to save the recommendation and context to a CSV file
    print('\n')
    save_recs.save_recs(conditions, scene, rec)


if __name__ == "__main__":
    asyncio.run(main())